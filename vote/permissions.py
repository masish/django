from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated, BasePermission, SAFE_METHODS


class IsAdmin(BasePermission):
    def has_permission(self, request, view):

        if (request.user.is_anonymous is False):
            if (request.user.email == 'haru_5175@yahoo.co.jp'):
                return True

        return False


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or IsAdmin().has_permission(request, view)


# 投票を行った人でないと更新、削除できない。
class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.user == request.user
