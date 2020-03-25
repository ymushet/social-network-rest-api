from django.conf.urls import url, include
from rest_framework import routers
from .views import UserRegisterView

router = routers.DefaultRouter()

router.register('register', UserRegisterView)

urlpatterns = [
    url('', include(router.urls)),
]