from rest_framework import permissions


class IsAdminAuthPermission(permissions.BasePermission):
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_active or request.user.is_staff)


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user==obj.author


class IsSellerOdAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user==obj.seller or request.user.is_staff