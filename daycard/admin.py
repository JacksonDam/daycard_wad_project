from django.contrib import admin
from daycard.models import Friendship, UserProfile
from daycard.models import DayCard

admin.site.register(Friendship)
admin.site.register(UserProfile)
admin.site.register(DayCard)