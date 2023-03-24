from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from daycard.models import DayCard, UserProfile, Friendship, Like
from django.utils import timezone
from django.test.client import RequestFactory
from .views import delete_daycard_handler, get_card_history, get_cards
from .views import post_daycard_handler, like_handler, friend_req_handler, friends_results_view

User = get_user_model()

def login_client(client):
	client.login(username="unittest12", password="unitunittest1212")

def make_post(self):
	self.profile.lastposted = timezone.now()
	self.profile.save()
	new_daycard = DayCard.objects.create(
		wordOne="unit",
		wordTwo="test",
		wordThree="west",
		caption="wow!",
		colour=1,
	    postUser=self.new_user 
	)
	new_daycard.save()

def make_posts(self):
	self.profile.lastposted = timezone.now()
	self.profile.save()
	new_daycard = DayCard.objects.create(
		wordOne="unit1",
		wordTwo="test1",
		wordThree="west1",
		caption="wow!1",
		colour=3,
	    postUser=self.new_user 
	)
	new_daycard.save()
	self.profile.lastposted = timezone.now()
	self.profile.save()
	new_daycard = DayCard.objects.create(
		wordOne="unit2",
		wordTwo="test2",
		wordThree="west2",
		caption="wow!2",
		colour=2,
	    postUser=self.new_user 
	)
	new_daycard.save()

def make_friends(user1, user2):
	new_friendship = Friendship.objects.create(user1=user1, user2=user2, user1Participating=True, user2Participating=True)
	new_friendship.save()

def make_friend_user():
	friend_user = User.objects.create_user(username="unittest13", email="un13@31un.com", first_name="unit2", last_name="test2", password="unitunittest1313")
	friend_user.save()
	friend_profile_user = UserProfile.objects.create(user=friend_user, firstname="unit2", lastname="test2", picture="test_imgs/alex.png", lastposted=None)
	friend_profile_user.save()
	return friend_user, friend_user.username, friend_profile_user

class TestViews(TestCase):
	def setUp(self):
		self.new_user = User.objects.create_user(username="unittest12", email="un12@21un.com", first_name="unit", last_name="test", password="unitunittest1212")
		self.new_user.save()
		self.profile = UserProfile.objects.create(user=self.new_user, firstname="unit", lastname="test", picture="test_imgs/alan.png", lastposted=None)
		self.profile.save()
		self.factory = RequestFactory()

	def test_logout_view(self):
		client = Client()
		response = client.get(reverse('logout'))
		self.assertRedirects(response, reverse('landing'), status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)		

	def test_signed_out_index_landing(self):
		client = Client()
		response = client.get(reverse('index'))
		self.assertRedirects(response, reverse('landing'), status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)

	def test_signed_in_index_home(self):
		client = Client()
		login_client(client)
		response = client.get(reverse('index'))
		self.assertRedirects(response, reverse('home'), status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)

	def test_landing_signed_out(self):
		client = Client()
		response = client.get(reverse('landing'))
		self.assertEquals(response.status_code, 200)
		self.assertTemplateUsed(response, 'daycard/landing.html')

	def test_landing_redirect_home_signed_in(self):
		client = Client()
		login_client(client)
		response = client.get(reverse('landing'))
		self.assertRedirects(response, reverse('home'), status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)

	def test_home_redirect_login_signed_out(self):
		client = Client()
		response = client.get(reverse('home'))
		self.assertRedirects(response, '/accounts/login/?next=/home/', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)

	def test_home_signed_in(self):
		client = Client()
		login_client(client)
		response = client.get(reverse('home'))
		self.assertEquals(response.status_code, 200)
		self.assertTemplateUsed('daycard/home.html')

	def test_friends_redirect_login_signed_out(self):
		client = Client()
		response = client.get(reverse('friends'))
		self.assertRedirects(response, '/accounts/login/?next=/friends/', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)

	def test_friends_signed_in(self):
		client = Client()
		login_client(client)
		response = client.get(reverse('friends'))
		self.assertEquals(response.status_code, 200)
		self.assertTemplateUsed('daycard/friends.html')

	def test_profile_redirect_login_signed_out(self):
		client = Client()
		response = client.get(reverse('profile'))
		self.assertRedirects(response, '/accounts/login/?next=/profile/', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)

	def test_post_redirect_login_signed_out(self):
		client = Client()
		response = client.get(reverse('post'))
		self.assertRedirects(response, '/accounts/login/?next=/post/', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)

	def test_post_signed_in_can_post(self):
		client = Client()
		login_client(client)
		response = client.get(reverse('post'))
		self.assertEquals(response.status_code, 200)
		self.assertTemplateUsed('daycard/post.html')

	def test_post_signed_in_cant_post_redirect_home(self):
		client = Client()
		login_client(client)
		self.profile.lastposted = timezone.now()
		self.profile.save()
		new_daycard = DayCard.objects.create(
			wordOne="unit",
			wordTwo="test",
			wordThree="west",
			caption="wow!",
			colour=1,
		    postUser=self.new_user 
		)
		new_daycard.save()
		response = client.get(reverse('post'))
		self.assertRedirects(response, reverse('home'), status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)

	def test_delete_current_daycard_with_no_daycard(self):
		client = Client()
		login_client(client)
		request = self.factory.get('/daycard/delete-daycard/')
		request.user = self.new_user
		response = delete_daycard_handler.as_view()(request)
		self.assertEquals(bytes.decode(response.content), "No DayCard to delete")

	def test_delete_current_daycard_with_daycard(self):
		client = Client()
		login_client(client)
		make_post(self)
		request = self.factory.get('/daycard/delete-daycard/')
		request.user = self.new_user
		response = delete_daycard_handler.as_view()(request)
		self.assertEquals(bytes.decode(response.content), "Deleted")

	def test_get_card_history_with_no_cards(self):
		client = Client()
		login_client(client)
		request = self.factory.get('/daycard/get-card-history/')
		request.user = self.new_user
		response = get_card_history.as_view()(request)
		self.assertContains(response, "No past DayCards found")

	def test_get_card_history_with_cards(self):
		client = Client()
		login_client(client)
		make_posts(self)
		request = self.factory.get('/daycard/get-card-history/')
		request.user = self.new_user
		response = get_card_history.as_view()(request)
		self.assertContains(response, 'class="card"', count=2)

	def test_get_cards_with_no_card(self):
		client = Client()
		login_client(client)
		request = self.factory.get('/daycard/get-cards/', {"sortmode": "false"})
		request.user = self.new_user
		response = get_cards.as_view()(request)
		self.assertContains(response, "No DayCards yet today!")

	def test_get_cards_with_card(self):
		client = Client()
		login_client(client)
		make_post(self)
		request = self.factory.get('/daycard/get-cards/', {"sortmode": "false"})
		request.user = self.new_user
		response = get_cards.as_view()(request)
		self.assertContains(response, 'class="card"', count=1)

	def test_post_daycard_handler_success(self):
		client = Client()
		login_client(client)
		request = self.factory.get('/daycard/post-new-daycard/', {"wordOne": "wow1", "wordTwo": "wow2", "wordThree": "wow3", "caption": "oh wow!", "colour": 1})
		request.user = self.new_user
		response = post_daycard_handler.as_view()(request)
		self.assertContains(response, "SUCCESS")		

	def test_post_daycard_handler_fail(self):
		client = Client()
		login_client(client)
		make_post(self)
		request = self.factory.get('/daycard/post-new-daycard/', {"wordOne": "wow1", "wordTwo": "wow2", "wordThree": "wow3", "caption": "oh wow!", "colour": 1})
		request.user = self.new_user
		response = post_daycard_handler.as_view()(request)
		self.assertContains(response, "ERROR")		

	def test_post_daycard_handler_fail_too_long(self):
		client = Client()
		login_client(client)
		request = self.factory.get('/daycard/post-new-daycard/', {"wordOne": "TwentyThreeCharacters123", "wordTwo": "wow2", "wordThree": "wow3", "caption": "oh wow!", "colour": 1})
		request.user = self.new_user
		response = post_daycard_handler.as_view()(request)
		self.assertContains(response, "ERROR")		

	def test_post_daycard_handler_fail_too_long_caption(self):
		client = Client()
		login_client(client)
		request = self.factory.get('/daycard/post-new-daycard/', {"wordOne": "wow1", "wordTwo": "wow2", "wordThree": "wow3", "caption": "oh wowowowowowowowowowowowowowowowowowowowowowowo!", "colour": 1})
		request.user = self.new_user
		response = post_daycard_handler.as_view()(request)
		self.assertContains(response, "ERROR")		

	def test_friend_req_handler_multistage(self):
		client = Client()
		login_client(client)
		friend_user, friend_username, friend_profile = make_friend_user()
		request1 = self.factory.get('/daycard/friend-req/', {"username": friend_username})
		request1.user = self.new_user
		response1 = friend_req_handler.as_view()(request1)	
		request2 = self.factory.get('/daycard/friend-req/', {"username": self.new_user.username})
		request2.user = friend_user
		response2 = friend_req_handler.as_view()(request2)
		request3 = self.factory.get('/daycard/friend-req/', {"username": self.new_user.username})
		request3.user = friend_user
		response3 = friend_req_handler.as_view()(request3)
		self.assertContains(response1, "CANCEL")	
		self.assertContains(response2, "REMOVE")		
		self.assertContains(response3, "ADD")	

	def test_friend_req_handler_fake_name(self):
		client = Client()
		login_client(client)
		friend_user, friend_username, friend_profile = make_friend_user()
		request1 = self.factory.get('/daycard/friend-req/', {"username": "wrong"})
		request1.user = self.new_user
		response1 = friend_req_handler.as_view()(request1)	
		self.assertContains(response1, "ERROR")	

	def test_like_handler_fail_with_nonfriend(self):
		client = Client()
		login_client(client)
		friend_user, friend_username, friend_profile = make_friend_user()
		request1 = self.factory.get('/daycard/like/', {"username": friend_username})
		request1.user = self.new_user
		response1 = like_handler.as_view()(request1)	
		self.assertEquals(bytes.decode(response1.content), "-1")		

	def test_like_handler_fail_with_friend_no_posts(self):
		client = Client()
		login_client(client)
		friend_user, friend_username, friend_profile = make_friend_user()
		make_friends(self.new_user, friend_user)
		request1 = self.factory.get('/daycard/like/', {"username": friend_username})
		request1.user = self.new_user
		response1 = like_handler.as_view()(request1)	
		self.assertEquals(bytes.decode(response1.content), "-1")	

	def test_like_handler_success_with_friend_with_posts(self):
		client = Client()
		login_client(client)
		friend_user, friend_username, friend_profile = make_friend_user()
		make_friends(self.new_user, friend_user)
		friend_profile.lastposted = timezone.now()
		friend_profile.save()
		new_daycard = DayCard.objects.create(
			wordOne="unit4",
			wordTwo="test4",
			wordThree="west4",
			caption="wow!4",
			colour=3,
		    postUser=friend_user
		)
		new_daycard.save()
		request1 = self.factory.get('/daycard/like/', {"username": friend_username})
		request1.user = self.new_user
		response1 = like_handler.as_view()(request1)	
		self.assertEquals(bytes.decode(response1.content), "1")	

	def test_like_handler_success_unlike_with_friend_with_posts(self):
		client = Client()
		login_client(client)
		friend_user, friend_username, friend_profile = make_friend_user()
		make_friends(self.new_user, friend_user)
		friend_profile.lastposted = timezone.now()
		friend_profile.save()
		new_daycard = DayCard.objects.create(
			wordOne="unit4",
			wordTwo="test4",
			wordThree="west4",
			caption="wow!4",
			colour=3,
		    postUser=friend_user
		)
		new_daycard.save()
		request1 = self.factory.get('/daycard/like/', {"username": friend_username})
		request1.user = self.new_user
		response1 = like_handler.as_view()(request1)	
		request2 = self.factory.get('/daycard/like/', {"username": friend_username})
		request2.user = self.new_user
		response2 = like_handler.as_view()(request2)	
		self.assertEquals(bytes.decode(response1.content), "1")	
		self.assertEquals(bytes.decode(response2.content), "0")	

	def test_friends_results_view_zero_length_query_friends(self):
		client = Client()
		login_client(client)
		friend_user, friend_username, friend_profile = make_friend_user()
		make_friends(self.new_user, friend_user)
		request1 = self.factory.get('/daycard/results/', {"query": ""})
		request1.user = self.new_user
		response1 = friends_results_view.as_view()(request1)	
		self.assertContains(response1, friend_username, 2)	

	def test_friends_results_view_query_friends(self):
		client = Client()
		login_client(client)
		friend_user = User.objects.create_user(username="extremedifference", email="un23@71n.com", first_name="extreme", last_name="difference", password="unitunittest1414")
		friend_user.save()
		friend_profile_user = UserProfile.objects.create(user=friend_user, firstname="extreme", lastname="difference", picture="test_imgs/alexis.png", lastposted=None)
		friend_profile_user.save()
		make_friends(self.new_user, friend_user)
		request1 = self.factory.get('/daycard/results/', {"query": "extremedifference"})
		request1.user = self.new_user
		response1 = friends_results_view.as_view()(request1)	
		self.assertContains(response1, friend_user.username, 2)	

	def test_friends_results_view_find_accept(self):
		client = Client()
		login_client(client)
		friend_user = User.objects.create_user(username="extremedifference", email="un23@71n.com", first_name="extreme", last_name="difference", password="unitunittest1414")
		friend_user.save()
		friend_profile_user = UserProfile.objects.create(user=friend_user, firstname="extreme", lastname="difference", picture="test_imgs/alexis.png", lastposted=None)
		friend_profile_user.save()
		new_friendship = Friendship.objects.create(user1=friend_user, user2=self.new_user, user1Participating=True, user2Participating=False)
		new_friendship.save()		
		request1 = self.factory.get('/daycard/results/', {"query": "extremedifference"})
		request1.user = self.new_user
		response1 = friends_results_view.as_view()(request1)	
		self.assertContains(response1, "ACCEPT", 1)	