from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.index, name='index'),
    path('timeline/<username>/', views.profile, name='profile'),
    path('<username>/following/', views.profile_follows, name='profile_follows'),
    path('<username>/followers/', views.profile_followers, name='profile_followers'),
    path('tweet/<int:tweet_id>', views.show_tweet, name='tweet'),
    path('follow/<int:followee_id>/', views.follow, name='follow'),
    path('unfollow/<int:followee_id>/', views.unfollow, name='unfollow'),
    path('login/', auth_views.LoginView.as_view(), name='main_login'),
    path('logout/', auth_views.LogoutView.as_view(), name='main_logout'),
]


	