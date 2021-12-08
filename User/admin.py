from django.contrib import admin
from User.models import UserModel, Song, Watchlater, History, Channel

admin.site.register(UserModel)
admin.site.register(Song)
admin.site.register(Watchlater)
admin.site.register(History)
admin.site.register(Channel)