# # # movie_app/tests.py

# from django.test import TestCase, Client
# from django.urls import reverse
# from rest_framework import status
# from rest_framework.test import APIClient
# from django.contrib.auth.models import User
# from .models import Collection, Movie
# import json
# import requests
# import ssl
# from requests.adapters import HTTPAdapter
# from requests.packages.urllib3.poolmanager import PoolManager

# # Define a custom SSL adapter
# # class SSLAdapter(HTTPAdapter):
# #     def init_poolmanager(self, *args, **kwargs):
# #         context = ssl.create_default_context()
# #         context.check_hostname = False
# #         context.verify_mode = ssl.CERT_NONE
# #         kwargs['ssl_context'] = context
# #         return super().init_poolmanager(*args, **kwargs)

# # # Configure requests to use the SSL adapter for HTTPS requests
# # requests.Session().mount('https://', SSLAdapter())


# class MovieCollectionTests(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.user = User.objects.create_user(username='testuser', password='testpass')
#         self.access_token = self.get_access_token()  # Store access token after authentication
#         # self.client.force_authenticate(user=self.user)

#     def get_access_token(self):
#         url = reverse('register')  # Adjust if using login endpoint
#         data = {'username': 'testuser', 'password': 'testpass'}
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertIn('access_token', response.data)
#         return response.data['access_token']

#     def test_register(self):
#         url = reverse('register')
#         data = {'username': 'newuser', 'password': 'newpass'}
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertIn('access_token', response.data)

#     def test_movie_list(self):
#         url = reverse('movie-list')
#         headers = {'Authorization': f'Bearer {self.access_token}'}
#         response = self.client.get(url, headers=headers)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertIn('data', response.data)

#     # def test_movie_list(self):
#     #     url = reverse('movie-list')
#     #     response = self.client.get(url)
#     #     self.assertEqual(response.status_code, status.HTTP_200_OK)
#     #     self.assertIn('data', response.data)

#     def test_create_collection(self):
#         url = reverse('collection-list')
#         data = {
#             'title': 'My Collection',
#             'description': 'A test collection',
#             'movies': [
#                 {
#                     'title': 'Test Movie',
#                     'description': 'A test movie',
#                     'genres': 'Action,Drama',
#                     'uuid': '123e4567-e89b-12d3-a456-426614174000'
#                 }
#             ]
#         }
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertIn('collection_uuid', response.data)

#     def test_get_collections(self):
#         url = reverse('collection-list')
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertIn('is_success', response.data)
#         self.assertIn('data', response.data)

#     def test_update_collection(self):
#         collection = Collection.objects.create(user=self.user, title='Test Collection', description='Test Description')
#         url = reverse('collection-detail', kwargs={'pk': collection.uuid})
#         data = {
#             'title': 'Updated Collection',
#             'description': 'Updated Description'
#         }
#         response = self.client.put(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['title'], 'Updated Collection')

#     def test_delete_collection(self):
#         collection = Collection.objects.create(user=self.user, title='Test Collection', description='Test Description')
#         url = reverse('collection-detail', kwargs={'pk': collection.uuid})
#         response = self.client.delete(url)
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

#     def test_request_count(self):
#         url = reverse('request-count')
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertIn('requests', response.data)

#     def test_reset_request_count(self):
#         url = reverse('reset-request-count')
#         response = self.client.post(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['message'], 'request count reset successfully')


from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from .models import Collection, Movie
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
import requests
import json
import ssl

class SSLAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        kwargs['ssl_context'] = context
        return super().init_poolmanager(*args, **kwargs)

# Mount the adapter to your requests session
requests.Session().mount('https://', SSLAdapter())

class MovieCollectionTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)

    def test_register(self):
        url = reverse('register')
        data = {'username': 'newuser', 'password': 'newpass'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access_token', response.data)

    def test_movie_list(self):
        url = reverse('movie-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('data', response.data)

    def test_create_collection(self):
        url = reverse('collection-list')
        data = {
            'title': 'My Collection',
            'description': 'A test collection',
            'movies': [
                {
                    'title': 'Test Movie',
                    'description': 'A test movie',
                    'genres': 'Action,Drama',
                    'uuid': '123e4567-e89b-12d3-a456-426614174000'
                }
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('collection_uuid', response.data)

    def test_get_collections(self):
        url = reverse('collection-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('is_success', response.data)
        self.assertIn('data', response.data)

    def test_update_collection(self):
        collection = Collection.objects.create(user=self.user, title='Test Collection', description='Test Description')
        url = reverse('collection-detail', kwargs={'pk': collection.uuid})
        data = {
            'title': 'Updated Collection',
            'description': 'Updated Description'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Collection')

    def test_delete_collection(self):
        collection = Collection.objects.create(user=self.user, title='Test Collection', description='Test Description')
        url = reverse('collection-detail', kwargs={'pk': collection.uuid})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_request_count(self):
        url = reverse('request-count')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('requests', response.data)

    def test_reset_request_count(self):
        url = reverse('reset-request-count')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'request count reset successfully')