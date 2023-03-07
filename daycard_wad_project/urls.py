from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.urls import include
from django.urls import re_path
from django.urls import re_path as url
from daycard import views
from daycard.forms import UserProfileForm

urlpatterns = [
    path('', views.index),
    path('daycard/', include('daycard.urls')),
    path('home/', views.home, name='home'),
    path('friends/', views.friends, name='friends'),
    path('post/', views.post, name='post'),
    url(r'^accounts/register/$', views.CustomRegister.as_view(form_class=UserProfileForm), name='registration_register'),
    path('registration_complete/', views.registercomplete, name='registration_complete'),
    path('accounts/', include('registration.backends.simple.urls')),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)