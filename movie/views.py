from django.shortcuts import render, redirect
from .recommender import MovieRecommender
from .models import *
from .forms import MovieForm, CreateUserForm, CreateListForm
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


###################### LOGIN AND REGISTRATION ######################
####################################################################
def register_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)
                return redirect('login')

        context = {'form': form}
        return render(request, 'movie/register.html', context)


def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username or password is incorrect')

        context = {}
        return render(request, 'movie/login.html', context)


def logout_user(request):
    logout(request)
    return redirect('home')



###################### CRUD MOVIES & MOVIE LISTS ###################
####################################################################
@login_required(login_url='login')
def add_movie(request, pk):
    movie_name = request.GET['movie']
    movie_list = MovieList.objects.get(id=pk)

    recommender = MovieRecommender()
    movie_info = recommender.get_movie_info(str(movie_name))
    added_movie = Movie(movie_list=movie_list,
                        name=movie_name,
                        release_year=movie_info[1],
                        genres=movie_info[2],
                        director=movie_info[3],
                        cast=movie_info[4],
                        rating=movie_info[5],
                        plot=movie_info[6])
    added_movie.save()
    return HttpResponse('<script>history.back();</script>')

@login_required(login_url='login')
def remove_movie(request, pk):
    Movie.objects.get(id=pk).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def create_list(request):
    if request.method == "POST":
        user = User.objects.get(id=request.user.id)
        movie = request.POST.get('fname')
        movie_list = MovieList(user_name=user,
                               list_name=movie)
        movie_list.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def delete_list(request, pk):
    MovieList.objects.get(id=pk).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



###################### SEARCH AND DISPLAY MOVIES ###################
####################################################################
def search_movie(request):
    info_for_all_movies = []
    user_movie_lists = ''
    recommender = MovieRecommender()
    form = MovieForm(request.POST)

    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        user_movie_lists = user.movielist_set.all().order_by('list_name')

    if request.method == 'POST':
        if 'search_movie' in request.POST:
            movie = request.POST.get('name')
            movie = recommender.get_most_similar_input_movie(movie)
            if movie:
                movies = recommender.recommend_movie(movie)
                for movie in movies:
                    movie_info = recommender.get_movie_info(movie)
                    info_for_all_movies.append(movie_info)
            else:
                messages.info(request, 'We apologize, We could not find similar movies. Please try another movie')

    context = {'movies': info_for_all_movies,
               'user_movie_lists': user_movie_lists,
               'form': form}

    return render(request, 'movie/home.html', context)


@login_required(login_url='login')
def movie_lists(request):
    user = User.objects.get(id=request.user.id)
    user_movie_lists = user.movielist_set.all().order_by('list_name')
    context = {'user_movie_lists': user_movie_lists}
    return render(request, 'movie/movie_lists.html', context)


@login_required(login_url='login')
def movies(request, pk):
    movie_list = MovieList.objects.get(id=pk)
    movies_in_list = movie_list.movie_set.all().order_by('name')

    context = {'movies_in_list': movies_in_list}
    return render(request, 'movie/movies.html', context)
