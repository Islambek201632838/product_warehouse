from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'admin'

class IsBuyer(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'buyer'

class IsSeller(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'seller'

class IsSellerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'seller' or request.user and request.user.role == 'admin'
