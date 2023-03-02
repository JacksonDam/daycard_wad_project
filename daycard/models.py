from django.db import models
from django.conf import settings

class Friendship(models.Model):
	user1 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="first_user")
	user2 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="second_user")
	user1Participating = models.BooleanField()
	user2Participating = models.BooleanField()