from django.core import exceptions
from django.db import IntegrityError
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

from util.email_verifier import EmailVerifier
from .models import CustomUser
import requests


class ProfileSerializer(serializers.ModelSerializer):
    pass


class RegisterCustomUserSerializer(serializers.ModelSerializer):
    """"
    Serializer for User data
    """
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'password2')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.get('password')
        user = CustomUser.objects.create(
            email=validated_data.get('email'))
        # try:
        #     # validate password wih django password validators
        #     validate_password(password, user)
        # except exceptions.ValidationError as ve:
        #     raise serializers.ValidationError({'password': ve.error_list})
        user.set_password(password)
        user.save()
        return user

    #
    # def validate_email(self, value):
    #     """"
    #     Custom field level validation with hunter.co
    #     """
    #     verifier = EmailVerifier(value)
    #     if not verifier.is_valid():
    #         raise serializers.ValidationError(verifier.errors)

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            _error = {'password': 'passwords must match'}
            raise serializers.ValidationError(_error)
        return super().validate(attrs)
