import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'daycard_wad_project.settings')
import sys
import random

import django
django.setup()
from django.db.models import Q
from django.conf import settings
from django.contrib.auth import get_user_model
from daycard.models import DayCard, UserProfile, Friendship, Like

User = get_user_model()

example_pass = "verySecureUniquePassword32!"

example_names = [
	"Alan Williams",
	"Alex Mercado",
	"Michael White",
	"Erik Ruiz",
	"Amy Walls",
	"Patricia Miller",
	"Mike Merritt",
	"Jennifer Moyer",
	"Veronica Evans",
	"Gwendolyn Lynch",
	"Vanessa Watts",
	"Alexis Smith",
	"Melissa Dunn",
	"Jeffrey Gillespie",
	"Antonio Reyes"
]

example_daycards = [
	("delightful", "exciting", "incredible", "Had a wonderful dinner tonight!", 0),
	("amazing", "thrilling", "fantastic", "Just went skydiving for the first time!", 0),
	("beautiful", "enchanting", "magical", "Took a stroll through the park and saw the most stunning sunset!", 1),
	("refreshing", "invigorating", "energizing", "Started my day with a refreshing yoga session!", 0),
	("inspiring", "motivating", "encouraging", "Attended an inspiring TED talk and left feeling empowered!", 0),
	("interesting", "informative", "educational", "Learned something new today!", 1),
	("ordinary", "typical", "average", "Just another day at work.", 1),
	("pleasant", "satisfying", "enjoyable", "Had a nice chat with an old friend.", 1),
	("convenient", "efficient", "practical", "Used a new app to help me organize my tasks.", 1),
	("routine", "predictable", "monotonous", "Same old, same old.", 1),
	("frustrating", "annoying", "disappointing", "My computer crashed and I lost all my work.", 2),
	("tiring", "exhausting", "draining", "I had a long day at work and just want to sleep.", 2),
	("embarrassing", "awkward", "uncomfortable", "I tripped and fell in front of everyone at the party.", 2),
	("irritating", "bothersome", "troublesome", "My neighbor's dog won't stop barking.", 2),
	("disheartening", "discouraging", "demotivating", "I didn't get the job I applied for.", 2)
]

def add_user_from_name(name):
	split_name = name.split()
	first_name = split_name[0]
	last_name = split_name[1]
	user_name = first_name.lower() + last_name.lower() + str(random.randint(1, 99))
	email = user_name + "@tester.com"
	new_user = User.objects.create_user(username=user_name, email=email, first_name=first_name, last_name=last_name, password=example_pass)
	new_user.save()
	imgfile = "test_imgs/" + first_name.lower() + ".png"
	user_profile = UserProfile.objects.create(user=new_user, firstname=first_name, lastname=last_name, picture=imgfile, lastposted=None)
	user_profile.save()

def make_users():
	for name in example_names:
		add_user_from_name(name)

def make_posts():
	random.shuffle(example_daycards)
	for index, user in enumerate(User.objects.filter(is_superuser=False, is_staff=False)):
		new_daycard = DayCard.objects.create(
			wordOne=example_daycards[index][0],
			wordTwo=example_daycards[index][1],
			wordThree=example_daycards[index][2],
			caption=example_daycards[index][3],
			colour=example_daycards[index][4],
		    postUser=user 
		)
		new_daycard.save()

def make_friends_with_demo_users(username1):
	try:
		given_user = User.objects.get(username=username1)
	except User.DoesNotExist:
		return None
	except ValueError:
		return None
	for index, user in enumerate(User.objects.filter(~Q(username=username1))):
		new_friendship = Friendship.objects.create(user1=given_user, user2=user, user1Participating=True, user2Participating=True)
		new_friendship.save()

def leave_random_likes_between_all(username1):
	for index, user in enumerate(User.objects.filter(~Q(username=username1))):
		all_other_users_daycards = list(DayCard.objects.filter(~Q(postUser=user)))
		random_amount_of_daycards = random.randint(1, len(example_daycards)-1)
		random_sample_of_daycards = random.sample(all_other_users_daycards, random_amount_of_daycards)
		for daycard in random_sample_of_daycards:
			new_like = Like.objects.create(likeUser=user, likedDayCard=daycard)
			new_like.save()

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print("Make a superuser or user and specify their username as a command line argument before running populate, so that you are friends with all demo users.")
		print("Exiting....")
		sys.exit()
	print("Starting population script....")
	make_users()
	make_posts()
	make_friends_with_demo_users(sys.argv[1])
	leave_random_likes_between_all(sys.argv[1])
	print("Population script complete.")