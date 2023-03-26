from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from take_me_app.views.auth import signup, me, UserViewSet

router = DefaultRouter()
router.register('', UserViewSet)

urlpatterns = [
    path('signup/', signup),
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('me/', me),
    # path('v1/stats', total)
]
urlpatterns.extend(router.urls)