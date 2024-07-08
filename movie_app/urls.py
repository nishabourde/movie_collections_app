# # movie_app/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'collection', views.CollectionViewSet, basename='collection')

urlpatterns = [
    path('register/', views.register, name='register'),
    path('movies/', views.movie_list, name='movie-list'),
    path('', include(router.urls)),
    path('collections/<uuid:collection_id>/add_movie/', views.add_movie_to_collection, name='add-movie-to-collection'),
    path('collections/', views.list_collections, name='list-collections'),
    path('request-count/', views.request_count, name='request-count'),
    path('request-count/reset/', views.reset_request_count, name='reset-request-count'),
]

# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from . import views

# router = DefaultRouter()
# router.register(r'collection', views.CollectionViewSet)

# urlpatterns = [
#     path('register/', views.register),
#     path('movies/', views.movie_list),
#     path('', include(router.urls)),
#     path('request-count/', views.request_count),
#     path('request-count/reset/', views.reset_request_count),
# ]