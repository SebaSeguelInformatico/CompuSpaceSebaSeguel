from django import forms
from .models import User,componente
from django.contrib.auth.forms import UserCreationForm



class UserForm(UserCreationForm):
    pass

    class Meta:
        model=User
        fields=['username','first_name','last_name','rut','email','region','comuna','direccion','password1','password2']

class componenteForm(forms.ModelForm):
    pass

    class Meta:
        model = componente
        fields=['nombre','marca','precio','stock']