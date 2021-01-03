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
    user_movie_lists = user.movielist_set.all().order_by('list_name')

    context = {'user_movie_lists': user_movie_lists}
    return render(request, 'movie/movie_lists.html', context)

@login_required(login_url='login')
def movies(request, pk):
    movie_list = MovieList.objects.get(id=pk)
    movies_in_list = movie_list.movie_set.all().order_by('name')


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


def add_movie_to_list(request, pk):
    print("HELOOOOOOOOOO")
    # print("MOVIE: ", key)
    print(request.GET.get('movie'))
    if request.method == "GET":
        print("MOVIE LIST: ", pk)

    # movie = Movie.objects.get(id=pk)
    # movie_list = MovieList.objects.get(id=pk2)

    return redirect('home')




def search_movie(request):

    info_for_all_movies = []
    recommender = MovieRecommender()
    form = MovieForm(request.POST)

    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        user_movie_lists = user.movielist_set.all().order_by('list_name')


    if request.method == 'POST':

        if 'search_movie' in request.POST:
            movie = request.POST.get('name')
            movies = recommender.recommend_movie(movie)
            for movie in movies:
                movie_info = recommender.get_movie_info(movie)
                info_for_all_movies.append(movie_info)
                # print(info_for_all_movies)

    # if request.method == 'GET':
        # print("USER MOVIE LISTS: ", user_movie_lists)

    if request.user.is_authenticated:
        context = {'movies': info_for_all_movies,
                   'user_movie_lists': user_movie_lists,
                   'form': form}
    else:
        context = {'movies': info_for_all_movies,
                   'form': form}
    return render(request, 'movie/dashboard.html', context)



@login_required(login_url='login')
def delete_list(request, pk):
    list_to_delete = MovieList.objects.get(id=pk)

    if request.method == 'POST':
        list_to_delete.delete()
        return redirect('movie_lists')

    context = {'list_to_delete': list_to_delete}
    return render(request, 'movie/delete_list.html', context)
