from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User


class CustomUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'photo_id']  # Add custom fields as needed


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'photo_id', 'cover_photo']  # Add custom fields as needed


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User  # Use the User model from Django's auth module
        fields = ['first_name', 'last_name', 'email']
