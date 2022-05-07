from django.shortcuts import render
from rest_framework.decorators import authentication_classes,permission_classes

from django.core.exceptions import ObjectDoesNotExist
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Tweets
from .serializers import TweetsSerializer, UserSerializer, FilterTweetSerializer, DeleteTweetSerializer
from django.contrib.auth.models import User

from rest_framework.response import Response
from rest_framework import status

class UsersAPI(ModelViewSet):
    '''
        This API is performs basic CRUD operation in the Users Model.
    '''

    serializer_class = UserSerializer
    queryset = User.objects.all()

    # This function is overridden because we need to authenticate the user before tweeting..
    def create(self,request):
        data = request.data
        serialized_data = UserSerializer(data=data)
        if serialized_data.is_valid():
            user = serialized_data.save()
            return Response(
                dict(
                    status = 'SUCCESS',
                    user_id = user.id,
                    created_timestamp = user.date_joined,
                ),status.HTTP_200_OK)
        else:
            return Response({'status':'FAILED'},status.HTTP_200_OK)


class TweetsAPI(ModelViewSet):
    '''
        This API needs BEARER Token in header for authentication
        Note: We also dont need username cause we can get that from the token
    '''

    authentication_classes = [JWTAuthentication]
    serializer_class = TweetsSerializer
    queryset = Tweets.objects.all()

    def create(self,request):
        data = dict(request.data)
        data['user_id'] = request.user.id
        serialized_data = TweetsSerializer(data=data)
        if serialized_data.is_valid():
            tweet = serialized_data.save()
            return Response(
                dict(
                    status = 'SUCCESS',
                    tweet_id = tweet.id,
                    created_timestamp = tweet.created_timestamp,
                ),status.HTTP_200_OK)
        else:
            return Response({'status':'FAILED'},status.HTTP_500_INTERNAL_SERVER_ERROR)

class FilterTweetAPI(APIView):
    '''
    This API needs username and from_date and returns the tweets of that user that has
    been created after the provided date
    '''

    serializer_class = FilterTweetSerializer
    permission_classes= [IsAuthenticated]

    def post(self,request):
        username = request.data.get('username')
        from_date = request.data.get('from_date')
        tweets = Tweets.objects.filter(user__username=username,created_timestamp__gte=from_date)
        serialized_data = TweetsSerializer(tweets,many=True)
        return Response(
                dict(
                    status='SUCCESS',
                    count=tweets.count(),
                    tweets = serialized_data.data,
                ),status.HTTP_200_OK)

class DeleteTweetAPI(APIView):
    serializer_class = DeleteTweetSerializer
    permission_classes = [IsAuthenticated]

    def post(self,request):
        username = request.data.get('username')
        tweets_deleted = Tweets.objects.filter(user__username=username)
        data = [{data.id:data.tweet} for data in tweets_deleted]
        tweets_deleted.delete()
        return Response(
                dict(
                    status = 'SUCCESS',
                    no_of_tweets_deleted = len(data),
                    data = data,
                ),status.HTTP_200_OK)
