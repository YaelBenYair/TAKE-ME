from rest_framework.routers import DefaultRouter

from take_me_app.views.challenge import CreateChallengeViewSet

router = DefaultRouter()
router.register('', CreateChallengeViewSet)

urlpatterns = [
    # path('create/', create_business),
]
urlpatterns.extend(router.urls)








