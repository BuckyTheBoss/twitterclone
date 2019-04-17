from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	img = models.ImageField(upload_to='media/images/',default=None, null=True, blank=True)
	bio = models.TextField(max_length=500, blank=True)
	birth_date = models.DateField(null=True, blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Tweet(models.Model):
	content = models.CharField(max_length=200)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	timestamp = models.DateTimeField(default=timezone.now)

class TweetComment(models.Model):
	content = models.CharField(max_length=200)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	timestamp = models.DateTimeField(default=timezone.now)
	tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)

class TweetMedia(models.Model):
	tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
	img = models.ImageField(upload_to='media/images/',default=None, null=True, blank=True)

class Follow(models.Model):
	follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
	followee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followee')
	timestamp = models.DateTimeField(default=timezone.now)