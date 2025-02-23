from django.template.context_processors import request
from rest_framework import permissions

class CheckStatus(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.status == 'client':
            return True
        return False


class CheckUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.status == 'owner':
            return True
        return False


class CheckStoreOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user == obj.owner:
            return True
        return False