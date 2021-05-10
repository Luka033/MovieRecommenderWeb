import difflib
import pandas as pd
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from movie_recommender.settings import STATICFILES_DIRS


class MovieRecommender:
    def __init__(self):
        self.df = pd.read_csv(os.path.join(
            STATICFILES_DIRS[0], 'data/IMDB_movie_posters.csv'))
        self.df = self.df.head(5000)
        # self.features = ['keywords', 'cast', 'genres', 'director']
        self.features = ['keywords', 'genres']

        for feature in self.features:
            self.df[feature] = self.df[feature].fillna('')

        self.df['combined_features'] = self.df.apply(
            self.combine_features, axis=1)

    def combine_features(self, row):
        try:
            return row['keywords'] + " " + row['genres']
        except:
            print("Error: ", row)

    def get_movie_info(self, requested_movie_info):
        all_movie_info = ""
        for index, movie in enumerate(self.df['original_title']):
            if movie == requested_movie_info:
                all_movie_info = [str(movie),
                                  str(self.df['release_year'][index]),
                                  str(self.df['genres'][index]),
                                  str(self.df['director'][index]),
                                  str(self.df['cast'][index]),
                                  str(self.df['vote_average'][index]),
                                  str(self.df['overview'][index]),
                                  str(self.df['image_posters'][index])
                                  ]

        return all_movie_info

    def get_most_similar_input_movie(self, input_movie):
        most_similar_input_movie = difflib.get_close_matches(
            input_movie, self.df['original_title'], n=1)

        return most_similar_input_movie[0] if len(most_similar_input_movie) else None

    def recommend_movie(self, movie_user_likes):
        cv = CountVectorizer()
        count_matrix = cv.fit_transform(self.df['combined_features'])
        cosine_sim = cosine_similarity(count_matrix)

        movie_index = self.get_index_from_title(movie_user_likes)
        similar_movies = list(enumerate(cosine_sim[movie_index]))

        sorted_similar_movies = sorted(
            similar_movies, key=lambda x: x[1], reverse=True)

        best_movies = []
        i = 0
        for movie in sorted_similar_movies:
            best_movies.append(self.get_title_from_index(movie[0]))
            i = i + 1
            if i >= 40:
                break

        return best_movies

    def get_title_from_index(self, index):
        return self.df[self.df.index == index]["original_title"].values[0]

    def get_index_from_title(self, title):
        return self.df[self.df.original_title == title]["index"].values[0]
