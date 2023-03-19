from django.urls import path
from daycard import views

app_name = 'daycard'

urlpatterns = [
	path('post-new-daycard/', views.post_daycard_handler.as_view(), name="post-new-daycard"),
	path('results/', views.friends_results_view.as_view(), name="results"),
	path('friend-req/', views.friend_req_handler.as_view(), name="friend-req"),
	path('like/', views.like_handler.as_view(), name="like"),
	path('home/', views.home, name='home'),
]