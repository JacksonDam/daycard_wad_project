from django.contrib import admin
from django.urls import path
from django.urls import include
from daycard import views

urlpatterns = [
    path('', views.index, name='index'),
    path('daycard/', include('daycard.urls')),
    path('admin/', admin.site.urls),
]
