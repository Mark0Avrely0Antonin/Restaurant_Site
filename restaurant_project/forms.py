from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from .models import *

import django_filters


class Menu_Filter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr = 'icontains', widget = forms.TextInput(
        attrs = {'class': 'form-control', 'style': 'width: 400px;'}))
    price = django_filters.NumberFilter(
        widget = forms.NumberInput(attrs = {'class': 'form-control', 'style': 'width: 350px;'}))
    price__gt = django_filters.NumberFilter(field_name = 'price', lookup_expr = 'gt', widget = forms.NumberInput(
        attrs = {'class': 'form-control', 'style': 'width: 300px;'}))
    price__lt = django_filters.NumberFilter(field_name = 'price', lookup_expr = 'lt', widget = forms.NumberInput(
        attrs = {'class': 'form-control', 'style': 'width: 300px;'}))




    class Meta:
        product = Menu


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'country', 'account_image', 'profile_username')


class LoginForm(AuthenticationForm):
    username = forms.CharField(label = 'Почта пользователя',
                               widget = forms.TextInput(
                                   attrs = {'class': 'form-control', 'style': 'width: 350px;'}))
    password = forms.CharField(label = 'Пароль пользователя',
                               widget = forms.PasswordInput(
                                   attrs = {'class': 'form-control', 'style': 'width:315px;'}))


class RegisterForm(UserCreationForm):
    username = forms.CharField(label = 'Имя пользователя',
                               widget = forms.TextInput(
                                   attrs = {'class': 'form-control', 'style': 'width:400px;'}))
    email = forms.EmailField(label = 'Почта пользователя',
                             widget = forms.EmailInput(attrs = {'class': 'form-control', 'style': 'width:375px;'}))

    # profile_username = forms.SlugField(label = 'Профильное имя',
    #                                    widget = forms.TextInput(
    #                                        attrs = {'class': 'form-control', 'style': 'width:350px;'}))

    password1 = forms.CharField(label = 'Пароль пользователя', widget = forms.PasswordInput(
        attrs = {'class': 'form-control', 'style': 'width:300px;'}))
    password2 = forms.CharField(label = 'Подтверждение пароля пользователя', widget = forms.PasswordInput(
        attrs = {'class': 'form-control', 'style': 'width:300px;'}))




    class Meta:
        model = User_Account
        fields = ('username', 'email', 'password1', 'password2')


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Reviews
        fields = ('content',)


class ContactsForm(forms.ModelForm):
    class Meta:
        model = ContactReview
        fields = ('comment',)
