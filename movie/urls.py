from django.urls import path
from . import views

urlpatterns = [
    path('', views.search_movie, name="home"),
    path('movie_lists/', views.movie_lists, name="movie_lists"),
    path('movies/<str:pk>', views.movies, name="movies"),

    path('add_movie/<str:pk>', views.add_movie_to_list, name='add_movie'),

    path('create_list/', views.create_list, name="create_list"),
    path('delete_list/<str:pk>', views.delete_list, name="delete_list"),

    path('register/', views.register_page, name="register"),
    path('login/', views.login_page, name="login"),
    path('logout/', views.logout_user, name="logout"),

]