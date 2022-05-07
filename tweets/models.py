from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


def to_epoch():
    return int(now().timestamp())

class Tweets(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    tweet = models.CharField(max_length=240,blank=False,null=False)
    created_timestamp = models.DateTimeField(auto_now_add=True)
