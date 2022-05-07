from rest_framework import serializers
from .models import Tweets
from django.contrib.auth.models import User
#from rest_framework_simplejwt.tokens import RefreshToken

class TweetsSerializer(serializers.ModelSerializer):
    def __init__(self,*args,**kwargs):
        self.user_id = kwargs.get('data',{}).get('user_id')
        super().__init__(*args,**kwargs)

    def to_representation(self,instance):
        data = super().to_representation(instance)
        data['username'] = instance.user.username
        return data

    def create(self,data):
        return Tweets.objects.create(user_id=self.user_id,tweet=data['tweet'])

    class Meta:
        model = Tweets
        fields = ('tweet',)

class FilterTweetSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=10,required=True)
    from_date = serializers.DateField()

class DeleteTweetSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=10,required=True)

class UserSerializer(serializers.ModelSerializer):

    def to_representation(self,instance):
        data = super().to_representation(instance)
        del data['password']
        data['created_timestamp'] = instance.date_joined.strftime('%Y-%m-%d')
        return data

    class Meta:
        model = User
        fields = (
            "username",
            "password"
        )
