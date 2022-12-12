from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (APISignUp, ConfCodeAuthToken, UserViewSet)


router_v1 = SimpleRouter()
router_v1.register('users', UserViewSet, basename='users')

auth_urls = [
    path('signup/', APISignUp.as_view()),
    path('token/', ConfCodeAuthToken.as_view()),
]

urlpatterns = [
    path('v1/auth/', include(auth_urls)),
    path('v1/', include(router_v1.urls)),
]
