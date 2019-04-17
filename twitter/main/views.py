from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from .models import *
import random

def index(request):
	if request.user.is_authenticated:
		tweets = Tweet.objects.filter(user__id=random.choice(range(0,58)))
		return render(request, 'homepage.html', {'tweets' : tweets})
	return render(request, 'index.html')

def profile(request, username):
	profile = Profile.objects.filter(user__username=username).first()
	if request.method == 'POST':
		if request.FILES['profile_pic']:
			profile_pic = request.FILES['profile_pic']
			fs = FileSystemStorage(location='media/images', base_url='/media/images')
			filename = fs.save(profile_pic.name, profile_pic)
			uploaded_file_url = fs.url(filename)
			profile.img = uploaded_file_url
			profile.save()
	follow_list = Follow.objects.filter(followee=profile.user).all()
	follower = False
	if follow_list != None:
		for record in follow_list:
			if request.user == record.follower:
				follower = True
	return render(request, 'profile.html', {'profile' : profile, 'follower' : follower })

def follow(request, followee_id):
	followee = User.objects.get(pk=followee_id)
	if Follow.objects.filter(followee=followee, follower=request.user).first():
		#flash message that you are already following
		return redirect('profile', followee.username)
	follow_log = Follow(followee=followee, follower=request.user)
	follow_log.save()
	return redirect('profile', followee.username)

def unfollow(request, followee_id):
	followee = User.objects.get(pk=followee_id)
	record = Follow.objects.get(followee=followee, follower=request.user)
	record.delete()
	return redirect('profile', followee.username)

def profile_follows(request, username):
	user = User.objects.get(username=username)
	records = user.follower.all()
	return render(request, 'following.html', {'records' : records, 'user' : user})

def profile_followers(request, username):
	user = User.objects.get(username=username)
	records = Follow.objects.filter(followee=user).all()
	followee_record_list = user.follower.all()
	for record in records:
		print(record.follower)
		print(record.followee)
		if record.follower == user:
			record.following = True
		else:
			record.following = False
		print(record.following)
	return render(request, 'followers.html', {'records' : records, 'user' : user})


def show_tweet(request, tweet_id):
	tweet = Tweet.objects.get(pk=tweet_id)
	return render(request, 'tweet.html', {'tweet' : tweet})
