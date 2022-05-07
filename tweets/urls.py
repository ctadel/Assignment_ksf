from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import TweetsAPI, UsersAPI, FilterTweetAPI, DeleteTweetAPI
from rest_framework.permissions import IsAuthenticated
from asgiref.sync import sync_to_async

router = DefaultRouter()
router.register('users',UsersAPI,'users')
router.register('tweets',TweetsAPI,'tweets')

urlpatterns = [
        path('tweets/create/',sync_to_async(TweetsAPI.as_view({'post':'create'},permission_classes=[IsAuthenticated])),name='createTweet'),
        path('tweets/filter/',FilterTweetAPI.as_view(permission_classes=[IsAuthenticated]),name='filterTweet'),
        path('tweets/delete/',DeleteTweetAPI.as_view(permission_classes=[IsAuthenticated]),name='deleteTweet'),
        ] + router.urls
