from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.conf import settings
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth import logout
from daycard.forms import UserProfileForm, EditProfilePictureForm
from daycard.models import Friendship, UserProfile
from daycard.models import DayCard, Like
from django.views import View
from registration.backends.simple.views import RegistrationView
from django.db.models import Q
import urllib
import datetime
from django.utils import timezone

json_bool_to_pybool = {"false": False, "true": True}

User = get_user_model()

def get_profile(username):
	try:
		user = User.objects.get(username=username)
	except User.DoesNotExist:
		return None

	return UserProfile.objects.get_or_create(user=user)[0]

def add_profile_to_context(context_dict, username):
	profile = get_profile(username)
	if profile is not None:
		context_dict['profile'] = profile
	return context_dict

def index(request):
	if not request.user.is_authenticated:
		return redirect(reverse('auth_login'))
	else:
		return redirect(reverse('home'))

class CustomRegister(RegistrationView):
	form_class = UserProfileForm

	def register(self, form_class):
		new_user = super(CustomRegister, self).register(form_class)
		firstname = form_class.cleaned_data['firstname']
		lastname = form_class.cleaned_data['lastname']
		if 'picture' in self.request.FILES:
			picture = self.request.FILES['picture']
		else:
			picture = None
		lastposted = form_class.cleaned_data['lastposted']
		user_profile = UserProfile.objects.create(user=new_user, firstname=firstname, lastname=lastname, picture=picture, lastposted=lastposted)
		user_profile.save()
		return user_profile

def registercomplete(request):
	return redirect(reverse('home'))

def logout_view(request):
	logout(request)
	return redirect(reverse('home'))

def retrieve_friends(user):
	friendships = Friendship.objects.filter(Q(user1=user) | Q(user2=user)).filter(Q(user1Participating=True) & Q(user2Participating=True))
	friend_user_objs = []
	for friendship in friendships:
		if friendship.user1 != user:
			friend_user_objs.append(friendship.user1)
		else:
			friend_user_objs.append(friendship.user2)
	return friend_user_objs

def get_friendship(username1, username2):
	try:
		friend_user = User.objects.get(username=username1)
	except User.DoesNotExist:
		return None
	except ValueError:
		return None

	try:
		request_user = User.objects.get(username=username2)
	except User.DoesNotExist:
		return None
	except ValueError:
		return None

	friendship_started_by_username1 = Friendship.objects.filter(Q(user1 = friend_user) & Q(user2 = request_user))
	friendship_started_by_username2 = Friendship.objects.filter(Q(user1 = request_user) & Q(user2 = friend_user))
	if friendship_started_by_username1:
		return (friendship_started_by_username1[0], 2)
	elif friendship_started_by_username2:
		return (friendship_started_by_username2[0], 1)
	else:
		return None

def retrieve_friends_tuples(user):
	friendships = Friendship.objects.filter(Q(user1=user) | Q(user2=user))
	friend_user_objs = []
	for friendship in friendships:
		if friendship.user1 != user:
			friend_user_objs.append((friendship.user1, friendship, 2))
		else:
			friend_user_objs.append((friendship.user2, friendship, 1))
	return friend_user_objs

def find_users(query):
	if query != "":
		return User.objects.filter(username__icontains = query)
	else:
		return User.objects.none()

def determine_friendship_status(friendship, requester_user):
	if requester_user == 1:
		if friendship.user1Participating == True and friendship.user2Participating == True:
			status = "REMOVE"
		elif friendship.user1Participating == True and friendship.user2Participating == False:
			status = "CANCEL"
		elif friendship.user1Participating == False and friendship.user2Participating == True:
			status = "ACCEPT"
	elif requester_user == 2:
		if friendship.user2Participating == True and friendship.user1Participating == True:
			status = "REMOVE"
		elif friendship.user2Participating == True and friendship.user1Participating == False:
			status = "CANCEL"
		elif friendship.user2Participating == False and friendship.user1Participating == True:
			status = "ACCEPT"
	return status

class friends_results_view(View):
	def get(self, request):
		query = urllib.parse.unquote(request.GET['query']).replace(' ', '')
		profile_results = {}
		users_list = []
		status = "ADD"

		if len(query) == 0:
			user_results = retrieve_friends_tuples(request.user)

			for friendship_tup in user_results:
				user = friendship_tup[0]
				if user.username != request.user.username:
					profile = get_profile(user.username)
					friendship = friendship_tup[1]
					requester_user = friendship_tup[2]
					status = determine_friendship_status(friendship, requester_user)
					if profile is not None:
						users_list.append((user, profile, status))
					else:
						users.list.append((user, None, status))
		else:
			user_results = find_users(query)

			for user in user_results:
				if user.username != request.user.username:
					profile = get_profile(user.username)
					friendship_tuple = get_friendship(user.username, request.user.username)

					if friendship_tuple is not None:
						friendship = friendship_tuple[0]
						requester_user = friendship_tuple[1]
						status = determine_friendship_status(friendship, requester_user)

					if profile is not None:
						users_list.append((user, profile, status))
					else:
						users.list.append((user, None, status))

		context_dict = {"users" : users_list}
		return render(request, 'daycard/results.html', context=context_dict)

class friend_req_handler(View):
	def get(self, request):
		friend_name = urllib.parse.unquote(request.GET['username'])
		friendship_tuple = get_friendship(friend_name, request.user.username)
		if friendship_tuple is not None:
			friendship = friendship_tuple[0]
			requester_user = friendship_tuple[1]

			if requester_user == 1:
				request_from_status = friendship.user1Participating
				request_to_status = friendship.user2Participating
			elif requester_user == 2:
				request_from_status = friendship.user2Participating
				request_to_status = friendship.user1Participating

			if request_from_status == False and request_to_status == True:
				if requester_user == 1:
					friendship.user1Participating = True
				elif requester_user == 2:
					friendship.user2Participating = True
				friendship.save()
				return HttpResponse("REMOVE")
			elif request_from_status == True:
				friendship.delete()
				return HttpResponse("ADD")
			elif request_from_status == False and request_to_status == False:
				if requester_user == 1:
					friendship.user1Participating = True
				elif requester_user == 2:
					friendship.user2Participating = True
				friendship.save()
				return HttpResponse("CANCEL")
		else:
			try:
				friend_user = User.objects.get(username=friend_name)
			except User.DoesNotExist:
				return HttpResponse("ERROR")
			except ValueError:
				return HttpResponse("ERROR")

			new_friendship = Friendship.objects.create(user1=request.user, user2=friend_user, user1Participating=True, user2Participating=False)
			new_friendship.save()

			return HttpResponse("CANCEL")

def friends(request):
	context_dict = add_profile_to_context({}, request.user.username)
	return render(request, 'daycard/friends.html', context=context_dict)

def get_daycards_of_user(user):
	return DayCard.objects.filter(postUser=user)

def get_like_count_of_daycard(post):
	return len(Like.objects.filter(likedDayCard=post))

def user_likes_daycard(user, post):
	return (len(Like.objects.filter(likeUser=user).filter(likedDayCard=post)) > 0)

class like_handler(View):
	def get(self, request):
		post_uname = urllib.parse.unquote(request.GET['username'])
		if (post_uname != request.user.username):
			if get_friendship(post_uname, request.user.username) is None:
				return HttpResponse("-1")
		try:
			post_user = User.objects.get(username=post_uname)
		except User.DoesNotExist:
			return HttpResponse("-1")
		except ValueError:
			return HttpResponse("-1")
		user_posts = get_daycards_of_user(post_user)
		if len(user_posts) == 0:
			return HttpResponse("-1")
		today = datetime.date.today()
		most_recent_user_post = user_posts.order_by('-postTime')[0]
		mrup_time = most_recent_user_post.postTime
		if (mrup_time.date() == today):
			like_count = get_like_count_of_daycard(most_recent_user_post)
			existing_like_filter = Like.objects.filter(likeUser=request.user).filter(likedDayCard=most_recent_user_post)
			if len(existing_like_filter) > 0:
				existing_like = existing_like_filter[0]
				existing_like.delete()
				return HttpResponse(str(like_count - 1))
			else:
				new_like = Like.objects.create(likeUser=request.user, likedDayCard=most_recent_user_post)
				new_like.save()
				return HttpResponse(str(like_count + 1))
		else:
			return HttpResponse("-1")

def user_can_post(user, posts=None, profile=None):
	if posts is None:
		posts = get_daycards_of_user(user)
	if profile is None:
		profile = get_profile(user.username)
	if profile.lastposted is None:
		return True
	return (datetime.date.today().day != profile.lastposted.day)

def fetch_user_current_daycard(user):
	today = datetime.date.today()
	posts = get_daycards_of_user(user)
	if len(posts) > 0:
		today_post = posts.filter(postTime__date=today)
		if len(today_post) > 0:
			return today_post[0]
	return None

class post_daycard_handler(View):
	def get(self, request):
		if request.user.is_authenticated:
			posts = get_daycards_of_user(request.user)
			profile = get_profile(request.user.username)
			if (user_can_post(request.user, posts, profile)) == True:
				word1 = request.GET['wordOne']
				word2 = request.GET['wordTwo']
				word3 = request.GET['wordThree']
				caption = request.GET['caption']
				colour = request.GET['colour']
				profile.lastposted = timezone.now()
				profile.save()
				new_daycard = DayCard.objects.create(postUser=request.user, wordOne=word1, wordTwo=word2, wordThree=word3, caption=caption, colour=colour)
				new_daycard.save()
				return HttpResponse("SUCCESS")
		return HttpResponse("ERROR")

def get_daycards_of_friends(user, friends, sortmode=False):
	today = datetime.date.today()
	if len(friends) == 0:
		own_daycard = DayCard.objects.filter(postUser=user).filter(postTime__date=today)
		if len(own_daycard) > 0:
			profile = get_profile(user.username)
			if profile is not None:
				return [(own_daycard[0], profile, get_like_count_of_daycard(own_daycard[0]), user_likes_daycard(user, own_daycard[0]))]
			else:
				return [(own_daycard[0], None, get_like_count_of_daycard(own_daycard[0]), user_likes_daycard(user, own_daycard[0]))]
		else:
			return DayCard.objects.none()
	else:
		q_object = Q()
		for friend in friends:
			q_object |= Q(postUser=friend)

		q_object |= Q(postUser=user)
		if sortmode:
			daycards = DayCard.objects.filter(q_object).filter(postTime__date=today).order_by('colour', '-postTime')
		else:
			daycards = DayCard.objects.filter(q_object).filter(postTime__date=today).order_by('-postTime')

		daycard_prof_tuples = []
		for daycard in daycards:
			profile = get_profile(daycard.postUser.username)
			if profile is not None:
				daycard_prof_tuples.append((daycard, profile, get_like_count_of_daycard(daycard), user_likes_daycard(user, daycard)))
			else:
				daycard_prof_tuples.append((daycard, None, get_like_count_of_daycard(daycard), user_likes_daycard(user, daycard)))

		return daycard_prof_tuples

class get_cards(View):
	def get(self, request):
		if request.user.is_authenticated:
			sortmode = request.GET['sortmode']
			if sortmode in json_bool_to_pybool:
				sortmode = json_bool_to_pybool[sortmode]
			else:
				sortmode = False
			context_dict = {}
			friends = retrieve_friends(request.user)
			context_dict["daycards"] = get_daycards_of_friends(request.user, friends, sortmode)
			return render(request, 'daycard/cards.html', context=context_dict)

class get_card_history(View):
	def get(self, request):
		if request.user.is_authenticated:
			context_dict = {}
			user_daycards = get_daycards_of_user(request.user).order_by('-postTime')
			daycard_tups = []
			for daycard in user_daycards:
				daycard_tups.append((daycard, None, None))
			context_dict["daycards"] = daycard_tups
			context_dict["minimal"] = True
			return render(request, 'daycard/cards.html', context=context_dict)

class delete_daycard_handler(View):
	def get(self, request):
		if request.user.is_authenticated:
			current_daycard = fetch_user_current_daycard(request.user)
			if current_daycard is not None:
				current_daycard.delete()
				return HttpResponse("Deleted")
		return HttpResponse("No DayCard to delete")


def home(request):
	if not request.user.is_authenticated:
		return redirect(reverse('auth_login'))
	context_dict = add_profile_to_context({}, request.user.username)
	can_post = user_can_post(request.user, None, None)
	context_dict["can_post"] = (can_post)
	return render(request, 'daycard/home.html', context=context_dict)

def post(request):
	context_dict = add_profile_to_context({}, request.user.username)
	return render(request, 'daycard/post.html', context=context_dict)

def profile(request):
	if request.method == 'POST':
		form = EditProfilePictureForm(request.POST, request.FILES)
		if form.is_valid():
			if 'picture' in request.FILES:
				picture = request.FILES['picture']
				profile = get_profile(request.user.username)
				if profile is not None:
					profile.picture.delete()
					profile.picture = picture
					profile.save()
					return redirect(reverse('profile'))

	context_dict = add_profile_to_context({}, request.user.username)
	return render(request, 'daycard/profile.html', context=context_dict)