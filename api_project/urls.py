from django.urls import path, include

from .views import *

urlpatterns = [
    path('menu_list/', Menu_List.as_view(), name='menu_list'),
    path('menu_view/<int:pk>/', Menu_Retrieve.as_view(), name='menu_view'),
    path('menu_update/<int:pk>/', Menu_Update.as_view(), name='menu_update'),
    path('menu_destroy/<int:pk>/', Menu_Destroy.as_view(), name='menu_delete'),


    path('category_list/', Category_List.as_view(), name='category_list'),
]
