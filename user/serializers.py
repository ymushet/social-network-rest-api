from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from rest_framework import serializers, status

from util.email_verifier import EmailVerifier
from .models import CustomUser, Profile

VALIDATION_ERRORS = {
    'risky': 'Could not validate personal email, please use email with organisation domain.',
    'undeliverable': 'Could not validate email, please use existing email with organisation domain.',
    'unknown_error': 'Could not validate email. Please contact support to resolve this error'
}


class ProfileSerializer(serializers.ModelSerializer):
    data = serializers.JSONField(allow_null=True, source='profile_data',
                                 binary=True)

    class Meta:
        model = Profile
        fields = ('data',)


class RegisterCustomUserSerializer(serializers.ModelSerializer):
    """"
    Serializer for User data
    """
    password2 = serializers.CharField(write_only=True, required=True)
    profile = ProfileSerializer(read_only=True, allow_null=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'password2', 'profile')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.get('password')
        user = CustomUser.objects.create(
            email=validated_data.get('email'))
        try:
            # validate password wih django password validators
            validate_password(password, user)
        except exceptions.ValidationError as ve:
            raise serializers.ValidationError({'password': ve.error_list})
        user.set_password(password)
        user.save()
        return user

    def validate_email(self, value):
        """"
        Custom field level validation with hunter.co
        """
        verifier = EmailVerifier(value)
        if not verifier.is_valid():
            if verifier.errors:
                raise serializers.ValidationError(verifier.errors)
            error_code = verifier.data.get('result', 'unknown_error')
            if verifier.status_code == status.HTTP_200_OK:
                raise serializers.ValidationError({error_code:
                                                       VALIDATION_ERRORS[error_code]})
            else:
                # This errors are 'Payment required' or 'Rate limit' errors etc, they
                # logged in by the EmailVerifier and should not be exposed to a user.
                raise serializers.ValidationError({'unknown_error':
                                                       VALIDATION_ERRORS['unknown_error']})
        return value

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            _error = {'password': 'passwords must match'}
            raise serializers.ValidationError(_error)
        return super().validate(attrs)
