from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from ArtyProd.models import  ProjectRequest

class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(label='Prénom')
    last_name = forms.CharField(label='Nom')
    email = forms.EmailField(label='Adresse e-mail')
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name' , 'email')

class ProjectRequestForm(forms.ModelForm):
    class Meta:
        model = ProjectRequest
        exclude = ['user']
