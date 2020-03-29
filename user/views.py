from rest_framework import mixins, viewsets

from .models import CustomUser
from .serializers import RegisterCustomUserSerializer


class UserRegisterView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """"
    User register view
    This view will validate email, create user and profile instances and
    return this data to a user
    """
    queryset = CustomUser.objects.all()
    serializer_class = RegisterCustomUserSerializer
