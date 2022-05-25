from django.core.signals import request_finished

from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import *


@receiver(post_save, sender = User_Account)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(account = instance, profile_username = instance.profile_username)


@receiver(post_save, sender = User_Account)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
