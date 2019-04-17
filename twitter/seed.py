from main.models import *
from faker import Faker
from django.contrib.auth.models import User
import random

fake = Faker()

def gen_fname():
	return fake.first_name()

def gen_lname():
	return fake.last_name()

def gen_password():
	return fake.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True)

def gen_paragraph():
	return fake.paragraph(nb_sentences=5, variable_nb_sentences=True, ext_word_list=None)

def gen_sentance():
	return fake.sentence(nb_words=6, variable_nb_words=True, ext_word_list=None)

def pick_user():
	return random.choice(User.objects.all())

def gen_tweet():
	return random.choice(Tweet.objects.all())

def gen_datetime(datetime=None):
	if datetime != None:
		return fake.date_time_between(start_date=datetime, end_date="-18d", tzinfo=None)
	return fake.date_this_year(before_today=True, after_today=False)

def gen_birthdate():
	return fake.date_this_century(before_today=True, after_today=False)

def create_users(number):
	'''create x users'''
	for i in range(0, number):
		fname = gen_fname()
		lname = gen_lname()
		username = fname.lower() + lname.lower()
		user = User.objects.create_user(username=username, password=gen_password(), first_name=fname, last_name=lname)
		user.save()

def create_tweet(number):
	'''create x tweets assigned to random users'''
	for i in range(0, number):
		tweet = Tweet(
			content= gen_paragraph(),
			user= pick_user(),
			timestamp= gen_datetime()
			)
		tweet.save()

def create_comment(number):
	'''create x comments per tweet in db assigned to random users'''
	for i in range(0, number):
		for tweet in Tweet.objects.all():
			comment = TweetComment(
				content = gen_paragraph(),
				user = pick_user(),
				timestamp = gen_datetime(tweet.timestamp),
				tweet=tweet
				)
			comment.save()

def seed_profile():
	for profile in Profile.objects.exclude(pk=1).all():
		profile.img = '/media/images/765-default-avatar.png'
		profile.bio = gen_sentance()
		profile.birth_date = gen_birthdate()
		profile.save()