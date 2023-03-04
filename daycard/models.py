from django.db import models
from django.conf import settings

class Friendship(models.Model):
	user1 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="first_user")
	user2 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="second_user")
	user1Participating = models.BooleanField()
	user2Participating = models.BooleanField()

class UserProfile(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	firstname = models.CharField(max_length=30)
	lastname = models.CharField(max_length=30)
	picture = models.ImageField(upload_to="profile_images", blank=True)
	lastposted = models.DateField(auto_now=True)

	def __str__(self):
		return self.firstname + " " + self.lastname