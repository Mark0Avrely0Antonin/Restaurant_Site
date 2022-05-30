from django.shortcuts import render

from .serializers import *
from restaurant_project.models import *

from rest_framework import generics, permissions, serializers

from api_project.permissions import *


# Create your views here.


class Menu_List(generics.ListCreateAPIView):
    serializer_class = MenuSerializer
    permission_classes = (IsAdminOrRead,)

    def get_queryset(self):
        return Menu.objects.filter().order_by('-dish_likes')

    def perform_create(self, serializer):
        serializer.save()


class Menu_Retrieve(generics.RetrieveAPIView):
    serializer_class = MenuSerializer

    def get_queryset(self):
        return Menu.objects.filter(pk = self.kwargs['pk'])


class Menu_Update(generics.RetrieveUpdateAPIView):
    serializer_class = MenuSerializer
    permission_classes = (IsAdminOrRead,)

    def get_queryset(self):
        return Menu.objects.filter(pk = self.kwargs['pk'])

    def perform_update(self, serializer):
        serializer.save()


class Menu_Destroy(generics.RetrieveDestroyAPIView):
    serializer_class = MenuSerializer
    permission_classes = (IsAdminOrRead,)

    def get_queryset(self):
        return Menu.objects.filter(pk = self.kwargs['pk'])

    def perform_destroy(self, instance):
        instance.delete()


class Category_List(generics.ListAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.all()