import difflib
import pandas as pd
import numpy as np
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from movie_recommender.settings import BASE_DIR
from movie_recommender.settings import STATICFILES_DIRS

NUM_MOVIES_TO_DISPLAY = 20


class MovieRecommender:
    def __init__(self):
        # self.df = pd.read_csv(os.path.join(STATICFILES_DIRS[0], 'data/IMDB_movie_dataset.csv'))
        self.df = pd.read_csv(os.path.join(STATICFILES_DIRS[0], 'data/IMDB_movie_posters.csv'))

        self.features = ['keywords', 'cast', 'genres', 'director']
        for feature in self.features:
            self.df[feature] = self.df[feature].fillna('')

        self.df['combined_features'] = self.df.apply(self.combine_features, axis=1)

    def combine_features(self, row):
        """
        :params:    Takes row in the dataframe and combines features into a feature vector
        """
        try:
            return row['keywords'] + " " + row['cast'] + " " + row['genres'] + " " + row['director']
        except Exception as e:
            print("Error: ", e)

    def get_movie_info(self, requested_movie_info):
        """
        :params:    Takes in a movie
        :returns    Returns a list of information about the movie
        """
        all_movie_info = ""
        for index, movie in enumerate(self.df['original_title']):
            if movie == requested_movie_info:
                all_movie_info = [str(movie),
                                  str(self.df['director'][index]),
                                  str(self.df['cast'][index]),
                                  str(self.df['vote_average'][index]),
                                  str(self.df['overview'][index]),
                                  str(self.df['image_posters'][index])
                                  ]

        return all_movie_info

    def recommend_movie(self, movie_user_likes):
        """
        :params:    Takes in a movie to use cosine similarity and find similar movies
        :returns    Returns a list of movies similar to the input movie
        """
        new_movie_user_likes = difflib.get_close_matches(movie_user_likes, self.df['original_title'], n=1)[0]

        # Create count matrix from this new combined column
        cv = CountVectorizer()
        count_matrix = cv.fit_transform(self.df['combined_features'])

        # Compute the Cosine Similarity based on the count_matrix
        cosine_sim = cosine_similarity(count_matrix)

        # Get index of this movie from its title
        movie_index = self.get_index_from_title(new_movie_user_likes)
        similar_movies = list(enumerate(cosine_sim[movie_index]))

        # Get a list of similar movies in descending order of similarity score
        sorted_similar_movies = sorted(similar_movies, key=lambda x: x[1], reverse=True)

        # Print titles of first 30 movies
        best_movies = []
        i = 0
        for movie in sorted_similar_movies:
            best_movies.append(self.get_title_from_index(movie[0]))
            i = i + 1
            if i >= NUM_MOVIES_TO_DISPLAY:
                break

        return best_movies

    def get_title_from_index(self, index):
        """
        :params:    Takes in a movie index
        :returns    Returns the corresponding movie title
        """
        return self.df[self.df.index == index]["original_title"].values[0]

    def get_index_from_title(self, title):
        """
        :params:    Takes in a movie title
        :returns    Returns the corresponding movie index
        """
        return self.df[self.df.original_title == title]["index"].values[0]
