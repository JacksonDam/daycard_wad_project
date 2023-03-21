from django.urls import path
from daycard import views

app_name = 'daycard'

urlpatterns = [
	path('post-new-daycard/', views.post_daycard_handler.as_view(), name="post-new-daycard"),
	path('results/', views.friends_results_view.as_view(), name="results"),
	path('friend-req/', views.friend_req_handler.as_view(), name="friend-req"),
	path('get-cards/', views.get_cards.as_view(), name="cards"),
	path('get-card-history/', views.get_card_history.as_view(), name="card-history"),
	path('like/', views.like_handler.as_view(), name="like"),
	path('delete-daycard/', views.delete_daycard_handler.as_view(), name="delete-daycard"),
	path('home/', views.home, name='home'),
]