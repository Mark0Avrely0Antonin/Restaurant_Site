from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
# Register your models here.


admin.site.register(Menu)
admin.site.register(Category)


admin.site.register(User_Account)
admin.site.register(Profile)

admin.site.register(Reviews)
admin.site.register(ContactReview)