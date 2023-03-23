import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'daycard_wad_project.settings')

from django.core.files import File
import django
django.setup()

from django.conf import settings
from django.contrib.auth import get_user_model
from daycard.models import DayCard, UserProfile, Friendship, Like

User = get_user_model()

users = [
	("username", "email" "firstname", "lastname", "password"),
]