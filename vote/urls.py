from django.urls import include, path
from django.contrib import admin
from rest_framework.routers import DefaultRouter

from vote.views import GameViewSet, VoteCtrlViewSet, VoteReadViewSet

router = DefaultRouter()
router.register('games', GameViewSet)
router.register('votes', VoteCtrlViewSet)
router.register('lists', VoteReadViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]