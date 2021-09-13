from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(label='First name')
    last_name = forms.CharField(label='Last name')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']


class PasswordChangingForm(PasswordChangeForm):
    password_atrrs = {'class': 'form-control', 'type': 'password'}
    old_password = forms.CharField(label='Old Password', widget=forms.PasswordInput(attrs=password_atrrs))
    new_password1 = forms.CharField(label='New Password', widget=forms.PasswordInput(attrs=password_atrrs))
    new_password2 = forms.CharField(label='New password confirmation', widget=forms.PasswordInput(attrs=password_atrrs))

    class Meta:
        model = User
        field = ('old_password', 'new_password1', 'new_password2')
