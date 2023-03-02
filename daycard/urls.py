from django.urls import path
from daycard import views

app_name = 'daycard'

urlpatterns = [
	path('home/', views.home, name='home'),
]