# movie_app/models.py

from django.db import models
from django.contrib.auth.models import User
import uuid

class Collection(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='collections')

# class Movie(models.Model):
#     uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
#     # uuid = models.UUIDField(primary_key=True, editable=False)
#     # title = models.CharField(max_length=255)
#     title = models.CharField(max_length=100, default='Default Title')
#     description = models.TextField()
#     genres = models.CharField(max_length=255)
#     collections = models.ManyToManyField(Collection, related_name='movies')


class Movie(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100, default='Default Title')
    description = models.TextField()
    genres = models.CharField(max_length=255)
    collections = models.ManyToManyField(Collection, related_name='movies')

    def __str__(self):
        return self.title