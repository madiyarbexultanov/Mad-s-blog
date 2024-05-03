import uuid
from datetime import timedelta

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms
from django.utils.timezone import now


from users.models import User, EmailVerification




class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Please enter your username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Please enter your password'}))
    class Meta:
        model = User
        fields = ('username', 'password')

class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
    'class': 'form-control', 'placeholder': 'Please enter your first_name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
    'class': 'form-control', 'placeholder': 'Please enter your last_name'}))
    username = forms.CharField(widget=forms.TextInput(attrs={
    'class': 'form-control', 'placeholder': 'Please enter your username'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={
    'class': 'form-control', 'placeholder': 'Please enter your email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
    'class': 'form-control', 'placeholder': 'Please enter your password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
    'class': 'form-control', 'placeholder': 'Please confirm your password'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=True)
        expiration = now() + timedelta(hours=48)
        record = EmailVerification.objects.create(code = uuid.uuid4(), user = user, expiration = expiration)
        record.send_verification_email()
        return user