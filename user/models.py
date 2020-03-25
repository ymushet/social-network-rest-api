import json

import clearbit
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from socialnetwork.settings import CLEARBIT_API_KEY

clearbit.key = CLEARBIT_API_KEY


class CustomUser(AbstractUser):
    username = models.CharField(blank=True, null=True, default=None, max_length=10)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.email


class Profile(models.Model):
    """"
    Extended User model to save clearbit information with post_signal
    """
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_data = JSONField(blank=True, null=True, default=None)

    def __str__(self):
        return f'{self.user.email}'


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile_data = clearbit.Enrichment.find(email=instance.email, stream=True)
        if profile_data is not None:
            profile_data = json.dumps(dict(profile_data))
        Profile.objects.create(user=instance, profile_data=profile_data)

@receiver(post_save, sender=CustomUser)
def update_user_profile(sender, instance, created, **kwargs):
    instance.profile.save(**kwargs)
