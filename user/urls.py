from rest_framework import routers

from .views import UserRegisterView

router = routers.SimpleRouter()

router.register('register', UserRegisterView, basename='register')

urlpatterns = router.urls

