from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from take_me_app.views.business import *

router = DefaultRouter()
router.register('create/', BusinessCreateViewSet)
router.register('', BusinessViewSet)

urlpatterns = [
    # path('create/', create_business),
    path('<int:business_id>/challenge/', create_business_challenge),
    path('choose_me/', get_choose_me_business),
    path('challenge_me/', get_challenge_me_business),
]
urlpatterns.extend(router.urls)