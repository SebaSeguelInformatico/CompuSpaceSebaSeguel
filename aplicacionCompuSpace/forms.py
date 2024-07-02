from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm



class UserForm(UserCreationForm):
    pass

    class Meta:
        model=User
        fields=['username','first_name','last_name','rut','email','region','comuna','direccion','password1','password2']


