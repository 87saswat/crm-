from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import fields

from .models import Customer, Order


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email', 'password1', 'password2' ]


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields ='__all__'
        
class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user',]        