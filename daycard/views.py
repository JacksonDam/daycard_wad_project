from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.conf import settings
from django.urls import reverse
from django.contrib.auth import get_user_model
from daycard.models import Friendship
import urllib

User = get_user_model()

def index(request):
	if not request.user.is_authenticated:
		return redirect(reverse('auth_login'))
	else:
		return redirect(reverse('home'))

def home(request):
	if not request.user.is_authenticated:
		return redirect(reverse('auth_login'))
	context_dict = {}
	return render(request, 'daycard/home.html', context=context_dict)

def retrieve_friends(username):
	return Friendship.objects.filter(user1.username == username) | Friendship.objects.filter(user2.username == username)

def find_users(query):
	return User.objects.filter(username__icontains = query)

def friends(request):
	query = request.GET.get('query')
	if query is not None:
		result = find_users(query)
		context_dict = {"users" : result, "pretext" : query}
		print(urllib.parse.unquote(query))
		print(result)
	else:
		context_dict = {}
	return render(request, 'daycard/friends.html', context=context_dict)