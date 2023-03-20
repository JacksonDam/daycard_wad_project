from django import forms
from registration.forms import RegistrationForm
from daycard.models import UserProfile

class UserProfileForm(RegistrationForm):
	firstname = forms.CharField()
	lastname = forms.CharField()
	picture = forms.ImageField()
	lastposted = forms.DateField(initial=None, widget=forms.HiddenInput(), required=False)

class EditProfilePictureForm(forms.Form):
	picture = forms.ImageField()