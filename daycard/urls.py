from django.urls import path
from daycard import views

app_name = 'daycard'

urlpatterns = [
	path('results/', views.friends_results_view.as_view(), name="results"),
	path('home/', views.home, name='home'),
]