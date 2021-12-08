# accounts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('signout', views.signout,name='signout'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('add_detail', views.add_detail,name='add_detail'),
    path('profile', views.profile,name='profile'),
     path('songs/', views.songs, name='songs'),
    path('songs/<int:id>', views.songpost, name='songpost'),
    path('watchlater', views.watchlater, name='watchlater'),
    path('history', views.history, name='history'),
    path('c/<str:channel>', views.channel, name='channel'),
    path('upload', views.upload, name='upload'),
    path('likes/<int:pk>', views.like_view, name='like_song'),
    path('song/<int:pk>/delete',views.delete_song, name='song_delete'),
    # path('logout', views.logout, name='logout'),
]

