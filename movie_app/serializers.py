# movie_app/serializers.py

from rest_framework import serializers
from .models import Collection, Movie
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        # fields = ('title', 'description', 'genres', 'uuid')
        fields = '__all__'
        read_only_fields = ('uuid',) 

class CollectionSerializer(serializers.ModelSerializer):
    movies = MovieSerializer(many=True, required=False)

    class Meta:
        model = Collection
        fields = ['uuid', 'title', 'description', 'movies'] 
        # fields = ('title', 'description', 'uuid', 'movies')

    def create(self, validated_data):
        movies_data = validated_data.pop('movies', [])
        collection = Collection.objects.create(**validated_data)
        for movie_data in movies_data:
            movie, _ = Movie.objects.get_or_create(**movie_data)
            collection.movies.add(movie)
        return collection

    def update(self, instance, validated_data):
        movies_data = validated_data.pop('movies', None)
        instance = super().update(instance, validated_data)
        if movies_data is not None:
            instance.movies.clear()
            for movie_data in movies_data:
                movie, _ = Movie.objects.get_or_create(**movie_data)
                instance.movies.add(movie)
        return instance