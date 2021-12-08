from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import CharField, DateField, BooleanField
from django.db.models import ImageField
import datetime


class UserModel(User):
    birth_date = DateField(name="birth_date",blank=True, null=True)
    state = CharField(name="state",max_length=20,blank=True,null=True)
    city = CharField(name="city",max_length=20,blank=True,null=True)
    number = CharField(name="number",max_length=10,blank=True,null=True)
    profile_image = ImageField(name="profile_image",blank=True,upload_to='images/%Y/%m/%d/',default='https://www.gravatar.com/avatar/00000000000000000000000000000000?d=https%3A%2F%2Fexample.com%2Fimages%2Favatar.jpg')
    plan = CharField(name="plan",default="free",max_length=10)
    is_updated = BooleanField(name="is_updated",default=False)


class Song(models.Model):
    user = models.ForeignKey(to=UserModel, on_delete=models.CASCADE, blank=True)
    song_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=2000)
    singer = models.CharField(max_length=2000)
    tags = models.CharField(max_length=100)
    image = models.FileField(upload_to='images/music', default="")
    song = models.FileField(upload_to='music')
    movie = models.CharField(max_length=1000, default="")
    credit = models.CharField(max_length=100000, default="")
    upload_date = models.DateTimeField(default=datetime.datetime.now(), blank=True)
    like = models.ManyToManyField(User, related_name='like_song')

    def total_likes(self):
        return self.like.count()

    def __str__(self):
        return self.name
    
    

class Watchlater(models.Model):
    watch_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(to=UserModel, on_delete=models.CASCADE)
    video_id = models.CharField(max_length=10000000, default="")

class History(models.Model):
    hist_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(to=UserModel, on_delete=models.CASCADE)
    music_id = models.CharField(max_length=10000000, default="")

class Channel(models.Model):
    channel_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=1000)
    music = models.CharField(max_length=100000000)
