from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.conf import settings
from django.urls import reverse
from django.contrib.auth import get_user_model
from daycard.forms import UserProfileForm
from daycard.models import Friendship, UserProfile
from django.views import View
from registration.backends.simple.views import RegistrationView
from django.db.models import Q
import urllib

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

def home(request):
	if not request.user.is_authenticated:
		return redirect(reverse('auth_login'))
	context_dict = add_profile_to_context({}, request.user.username)
	return render(request, 'daycard/home.html', context=context_dict)

def retrieve_friends(username):
	return Friendship.objects.filter(Q(user1.username == username) | Q(user2.username == username))

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

def find_users(query):
	if query != "":
		return User.objects.filter(username__icontains = query)
	else:
		return User.objects.none()

class friends_results_view(View):
	def get(self, request):
		query = urllib.parse.unquote(request.GET['query']).replace(' ', '')
		user_results = find_users(query)
		profile_results = {}
		users_list = []

		for user in user_results:
			if user.username != request.user.username:
				profile = get_profile(user.username)
				friendship_tuple = get_friendship(user.username, request.user.username)
				status = "ADD"

				if friendship_tuple is not None:
					friendship = friendship_tuple[0]
					requester_user = friendship_tuple[1]
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

				if profile is not None:
					users_list.append((user, profile, status))
				else:
					users.list.append((user, None, status))

		context_dict = {"users" : users_list, "pretext" : query}
		print(query)
		print(find_users(query))
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