from rest_framework.routers import DefaultRouter
from django.urls import path, include

from take_me_app.views.challenge import *

router = DefaultRouter()
router.register('challenge_set', CreateChallengeViewSet)
router.register('who_to_challenge', WhoToChallengeViewSet, basename='who_to_challenge')
router.register('challenge_type', ChallengeTypeViewSet, basename='challenge_type')

urlpatterns = [
    # path('add_user_to_business_challenge/', add_users_to_exists_challenge),
    path('', include(router.urls)),
]
# urlpatterns += router.urls








