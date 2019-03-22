from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'required': 'true'
            }),

            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'required': 'true'
            }),
            'password': forms.TextInput(attrs={
                'type': 'password',
                'class': 'form-control',
                'required': 'true'
            }),
        }
 


class LoginForm(forms.Form):

    username = forms.CharField(max_length=30,
                               widget=forms.TextInput(attrs={
                                   'class': 'form-control',
                                   'placeholder':"Ingrese su Usuario",
                                   'required': 'true'
                               }))
    password = forms.CharField(max_length=30,
                               widget=forms.TextInput(attrs={
                                   'type': 'password',
                                   'class': 'form-control',
                                   'placeholder':"Ingrese su Password",
                                   'required': 'true'
                               }))





class RegistroForm(UserCreationForm):

  class Meta:
    model = User
    fields = [
        'username',
        'first_name',
        'last_name',
        'email',
      ]
    labels = {
        'username': 'Nombre de usuario',
        'first_name': 'Nombre',
        'last_name': 'Apellidos',
        'email': 'Correo',
    }


