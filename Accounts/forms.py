from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.forms import widgets
from django.forms import ModelForm, TextInput, EmailInput


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100,widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder': 'FirstName'
    }))
    last_name = forms.CharField(max_length=100,widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder': 'LastName'
    }) )
    email = forms.EmailField(max_length=100,widget=forms.EmailInput(attrs={
        'class':'form-control',
        'placeholder': 'Email'
    }))
    password1=forms.CharField(max_length=100,widget=forms.PasswordInput(attrs={
        'class':'form-control',
        'placeholder': 'Password'
    }))
    password2=forms.CharField(max_length=100,widget=forms.PasswordInput(attrs={
        'class':'form-control',
        'placeholder': 'Confirm Password'
    }))


    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
'email', 'password1', 'password2',)
        widgets= {
            'username': TextInput(attrs={
                'class': "form-control",
                'placeholder': 'Username'
                }),
              
        }


class LoginForm(AuthenticationForm):
    username=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    password =forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))