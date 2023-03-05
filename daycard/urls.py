from django.urls import path
from daycard import views

app_name = 'daycard'

urlpatterns = [
	path('results/', views.friends_results_view.as_view(), name="results"),
	path('friend-req/', views.friend_req_handler.as_view(), name="friend-req"),
	path('home/', views.home, name='home'),
]