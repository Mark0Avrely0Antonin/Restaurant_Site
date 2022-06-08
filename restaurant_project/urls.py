from django.urls import path, include

from .views import * 


urlpatterns = [


  path('main/', MenuView.as_view(), name='main'),
  path('category_menu/<int:category_id>/', get_category_menu, name='get_category_menu'),

  path('view_dish/<slug:slug>/', ViewMenu.as_view(), name='view_dish'),
  path('dish_likes/<slug:slug>/', dish_likes, name='dish_likes'),

  path('about_us/', AboutUs.as_view(), name='about_us'),

  path('register/', register, name='register'),
  path('login/', LoginView.as_view(), name='login'),
  path('logout/', LogoutView.as_view(), name='logout'),

  path('profile_view/<slug:slug>/', ProfileView.as_view(), name='profile_view'),

  path('edit_profile/<slug:slug>/', edit_profile, name='edit_profile'),


  path('contacts/', Contacts.as_view(), name='contacts'),
  path('comment/', CommentAddReview.as_view(), name='comment_add'),


  path('change_password/', ChangePassword.as_view(), name='change_password'),


  path('review/<int:pk>/', AddReview.as_view(), name='add_review'),
  path('review_likes/<slug:slug>/', review_likes, name='review_likes'),
  path('review_unlikes/<slug:slug>/', review_unlikes, name='review_unlikes'),


  path('activate_user/<uidb64>/<token>', activate_user, name='activate'),

  path("menu_filter/", menu_filter, name='menu_filter'),


]



