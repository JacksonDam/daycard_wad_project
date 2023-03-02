from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.urls import include
from daycard import views

urlpatterns = [
    path('', views.index),
    path('daycard/', include('daycard.urls')),
    path('home/', views.home, name='home'),
    path('friends/', views.friends, name='friends'),
    path('accounts/', include('registration.backends.simple.urls')),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)