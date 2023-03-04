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
		print("WE TRIED")
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
	return Friendship.objects.filter(user1.username == username) | Friendship.objects.filter(user2.username == username)

def find_users(query):
	if query != "":
		return User.objects.filter(username__icontains = query)
	else:
		return User.objects.none()

class friends_results_view(View):
	def get(self, request):
		query = urllib.parse.unquote(request.GET['query']).replace(' ', '')
		context_dict = {"users" : find_users(query), "pretext" : query}
		print(query)
		print(find_users(query))
		return render(request, 'daycard/results.html', context=context_dict)

def friends(request):
	context_dict = add_profile_to_context({}, request.user.username)
	return render(request, 'daycard/friends.html', context=context_dict)