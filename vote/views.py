from django.shortcuts import render

from rest_framework import viewsets
from .models import Game, Vote
from .serializers import GameSerializer, VoteCtrlSerializer, VoteReadSerializer
from rest_framework import permissions
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from vote.permissions import IsOwnerOrReadOnly, IsAdmin, IsAdminOrReadOnly
from django.core.exceptions import ValidationError


class GameViewSet(viewsets.ReadOnlyModelViewSet):
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    # permission_classes = (IsAdminOrReadOnly,)

    queryset = Game.objects.all()
    serializer_class = GameSerializer


class VoteCtrlViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                        IsOwnerOrReadOnly,)

    queryset = Vote.objects.all()
    serializer_class = VoteCtrlSerializer

    def perform_create(self, serializer):
        # ログインユーザーを投票のユーザーにする
        serializer.save(user=self.request.user)


class VoteReadViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Vote.objects.all()
    serializer_class = VoteReadSerializer
