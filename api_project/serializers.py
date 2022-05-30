from rest_framework import serializers

from restaurant_project.models import *


class MenuSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField(method_name = 'get_category')
    dish_likes = serializers.ReadOnlyField(source = 'dish_likes.count')




    class Meta:
        model = Menu
        fields = ('id', 'name', 'content', 'price', 'photo', 'category', 'url', 'dish_likes',)




    def get_category(self, obj):
        return obj.category.name


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name',)
