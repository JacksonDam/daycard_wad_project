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

class DayCard(models.Model):
	postTime = models.DateTimeField(auto_now=True)
	wordOne = models.CharField(max_length=20)
	wordTwo = models.CharField(max_length=20)
	wordThree = models.CharField(max_length=20)
	caption = models.CharField(max_length=45)
	colour = models.IntegerField()
	postUser = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

	class Meta:
		verbose_name_plural = "DayCards"