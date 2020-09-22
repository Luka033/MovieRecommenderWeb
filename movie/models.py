from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class MovieList(models.Model):
    user_name = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    list_name = models.CharField(max_length=200)

    def __str__(self):
        return self.list_name


class Movie(models.Model):
    movie_list = models.ForeignKey(MovieList, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

