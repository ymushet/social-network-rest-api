from django.db import models
from django.contrib.auth.models import AbstractUser
# from django.contrib.postgres.fields import HStoreField
# from django.contrib.postgres.validators import KeysValidator
# from django.db.models.signals import post_save
# from django.dispatch import receiver
#
# import clearbit


class CustomUser(AbstractUser):
    username = models.CharField(blank=True, null=True, default=None, max_length=10)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.email


# class Profile(AbstractUser):
#     """"
#     Extended User model to save clearbit information with post_signal
#     """
#     user = models.OneToOneField(AbstractUser, on_delete=models.CASCADE)
#     profile_data = HStoreField(validators=KeysValidator)
#
#
# @receiver(post_save, sender=AbstractUser)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         profile_data = clearbit.Person.find(email=instance.email)
#         Profile.objects.create(user=instance, profile_data=profile_data)
#
#
# @receiver(post_save, sender=AbstractUser)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save(**kwargs)
