from django.shortcuts import render, redirect
from .recommender import MovieRecommender
from .models import *
from .forms import MovieForm, CreateUserForm, CreateListForm
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url='login')
def movie_lists(request):
    user = User.objects.get(id=request.user.id)
    user_movie_lists = user.movielist_set.all()

    context = {'user_movie_lists': user_movie_lists}
    return render(request, 'movie/movie_lists.html', context)

@login_required(login_url='login')
def movies(request, pk):
    # print("LIST PK: ", pk)
    movie_list = MovieList.objects.get(id=pk)
    movies_in_list = movie_list.movie_set.all()


    context = {'movies_in_list': movies_in_list}
    return render(request, 'movie/movies.html', context)


@login_required(login_url='login')
def create_list(request):
    form1 = CreateListForm()
    if request.method == 'POST':
        user = User.objects.get(id=request.user.id)
        form = CreateListForm(request.POST)
        if form.is_valid():
            form1 = form.save(commit=False)
            form1.user_name = user
            form1.save()

        return redirect('movie_lists')

    context = {'form': form1}
    return render(request, 'movie/create_list.html', context)




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


def search_movie(request):
    movies = ""
    movie_info = ""
    info_for_all_movies = []
    recommender = MovieRecommender()
    form = MovieForm(request.POST)
    if request.method == 'POST':

        if 'search_movie' in request.POST:
            movie = request.POST.get('name')
            movies = recommender.recommend_movie(movie)
            for movie in movies:
                movie_info = recommender.get_movie_info(movie)
                info_for_all_movies.append(movie_info)

    if request.method == 'GET':
        info = request.GET.get('name')
        movie_info = recommender.get_movie_info(info)
        print("MOVIE INFO: ", movie_info)

    context = {'movies': info_for_all_movies, 'form': form}


    return render(request, 'movie/dashboard.html', context)




def testmodal(request):
    context = {}
    return render(request, 'movie/testmodal.html', context)
