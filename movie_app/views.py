# movie_app/views.py

from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .models import Collection, Movie
from .serializers import UserSerializer, CollectionSerializer, MovieSerializer
import requests
from django.conf import settings
from collections import Counter

@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'access_token': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def movie_list(request):
    url = settings.MOVIE_API_URL
    try:
        response = requests.get(url, verify=False)  # Note: Disabling SSL verification
        response.raise_for_status()
        return Response(response.json())
        # print(response.json())
    except requests.exceptions.RequestException as e:
        return Response({"Error": e})
    # auth = (settings.MOVIE_API_USERNAME, settings.MOVIE_API_PASSWORD)
    # response = requests.get(url, auth=auth)
    # if response.status_code == 200:
    #     return Response(response.json())
    # return Response({'error': 'Failed to fetch movies'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def movie_list(request):
#     url = settings.MOVIE_API_URL
#     auth = (settings.MOVIE_API_USERNAME, settings.MOVIE_API_PASSWORD)
#     response = requests.get(url, auth=auth)
#     if response.status_code == 200:
#         return Response(response.json())
#     return Response({'error': 'Failed to fetch movies'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CollectionViewSet(viewsets.ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # # def list(self, request):
    # #     collections = self.get_queryset()
    # #     serializer = self.get_serializer(collections, many=True)
        
    #     # Calculate top 3 favorite genres
    #     all_genres = []
    #     for collection in collections:
    #         for movie in collection.movies.all():
    #             all_genres.extend(movie.genres.split(','))
    #     top_genres = [genre for genre, _ in Counter(all_genres).most_common(3)]

    #     return Response({
    #         'is_success': True,
    #         'data': {
    #             'collections': serializer.data,
    #             'favourite_genres': ', '.join(top_genres)
    #         }
        # })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def request_count(request):
    count = request.session.get('request_count', 0)
    return Response({'requests': count})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reset_request_count(request):
    request.session['request_count'] = 0
    return Response({'message': 'request count reset successfully'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_movie_to_collection(request, collection_id):
    try:
        collection = Collection.objects.get(pk=collection_id)
    except Collection.DoesNotExist:
        return Response({'error': 'Collection not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = MovieSerializer(data=request.data)
    if serializer.is_valid():
        movie = serializer.save()
        collection.movies.add(movie)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_collections(request):
    collections = Collection.objects.filter(user=request.user)  # Filter collections for the current user
    serializer = CollectionSerializer(collections, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)