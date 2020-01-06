from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30,widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=30,widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    email = forms.EmailField(max_length=200,widget=forms.TextInput(attrs={'placeholder': 'E-mail'}))
    phone_number = forms.CharField(max_length=30,widget=forms.TextInput(attrs={'placeholder': 'Phone-number'}))
    password1=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Repeat Password'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'phone_number', 'email', 'password1', 'password2')
        widgets={
            
            'username': forms.TextInput(attrs={'placeholder':'Username'}),
        }
class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    email = forms.EmailField(max_length=200, widget=forms.TextInput(attrs={'placeholder': 'E-mail'}))
    class Meta:
        model = User
        fields = ('username', 'email')
class ProfileUpdateForm(forms.ModelForm):
    # phone_number = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Phone-number'}))
    class Meta:
        model = Profile
        fields = ('profile_picture', 'phone_number')