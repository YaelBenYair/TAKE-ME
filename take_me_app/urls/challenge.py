from rest_framework.routers import DefaultRouter
from django.urls import path

from take_me_app.views.challenge import CreateChallengeViewSet, add_users_to_business_challenge

router = DefaultRouter()
router.register('', CreateChallengeViewSet)

urlpatterns = [
    path('add_user_to_business_challenge/', add_users_to_business_challenge),
]
urlpatterns.extend(router.urls)








