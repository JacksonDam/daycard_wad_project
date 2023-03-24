from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from daycard.models import DayCard, UserProfile, Friendship, Like
import datetime

User = get_user_model()

class TestModels(TestCase):
	def setUp(self):
		self.new_user = User.objects.create_user(username="unittest12", email="un12@21un.com", first_name="unit", last_name="test", password="unitunittest1212")
		self.new_user.save()
		self.new_user2 = User.objects.create_user(username="unitt453454", email="un23412@23241un3.com", first_name="unit2", last_name="test2", password="unitun324ittest321212")
		self.new_user2.save()

	def test_friendship_model(self):
		new_friendship = Friendship.objects.create(user1=self.new_user, user2=self.new_user2, user1Participating=True, user2Participating=False)
		new_friendship.save()
		self.assertEquals(new_friendship.user1.username, "unittest12")
		self.assertEquals(new_friendship.user2.username, "unitt453454")
		self.assertTrue(new_friendship.user1Participating)
		self.assertFalse(new_friendship.user2Participating)

	def test_user_profile(self):
		profile = UserProfile.objects.create(user=self.new_user, firstname="unit", lastname="test", picture="test_imgs/amy.png", lastposted=None)
		profile.save()
		profile2 = UserProfile.objects.create(user=self.new_user2, firstname="unit2", lastname="test2", picture="test_imgs/antonio.png", lastposted=datetime.date.today())
		profile2.save()
		self.assertEquals(profile.user.username, "unittest12")
		self.assertEquals(profile2.user.username, "unitt453454")
		self.assertEquals(profile.firstname, "unit")
		self.assertEquals(profile2.firstname, "unit2")
		self.assertEquals(profile.lastname, "test")
		self.assertEquals(profile2.lastname, "test2")
		self.assertEquals(profile.picture, "test_imgs/amy.png")
		self.assertEquals(profile2.picture, "test_imgs/antonio.png")
		self.assertIsNone(profile.lastposted)
		self.assertEquals(profile2.lastposted, datetime.date.today())		

	def test_daycard(self):
		new_daycard = DayCard.objects.create(
			wordOne="unit5",
			wordTwo="test7",
			wordThree="west9",
			caption="wow!11",
			colour=2,
		    postUser=self.new_user 
		)
		new_daycard.save()
		self.assertEquals(new_daycard.wordOne, "unit5")
		self.assertEquals(new_daycard.wordTwo, "test7")
		self.assertEquals(new_daycard.wordThree, "west9")
		self.assertEquals(new_daycard.caption, "wow!11")
		self.assertEquals(new_daycard.colour, 2)
		self.assertEquals(new_daycard.postUser, self.new_user)

	def test_like(self):
		new_daycard = DayCard.objects.create(
			wordOne="unit8",
			wordTwo="test12",
			wordThree="west6356",
			caption="wow!5689",
			colour=1,
		    postUser=self.new_user 
		)
		new_daycard.save()
		new_like = Like.objects.create(likeUser=self.new_user, likedDayCard=new_daycard)
		new_like.save()
		self.assertEquals(new_like.likeUser, self.new_user)
		self.assertEquals(new_like.likedDayCard, new_daycard)