from django import forms
from django.contrib.auth.models import User
from django.db import models

from shop.models import Product, Comment, Order


class ProductModelForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ()


class CommentModelForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['full_name', 'email', 'message']


class OrderModelForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ('product',)


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True)

    def clean_username(self):
        username = self.data['username']
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError(f'that user {username} does not exist')
        return username







