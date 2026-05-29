# accounts/permissions.py (برای DRF)
from rest_framework import permissions

class IsSuperAdmin(permissions.BasePermission):
    """فقط سوپر ادمین (ادمین مطلق)"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_superuser


class IsAdminUser(permissions.BasePermission):
    """ادمین ضعیف یا قوی (هر کسی که role=admin یا is_superuser=True)"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.role == 'admin' or request.user.is_superuser)

class IsInstructor(permissions.BasePermission):
    """مدرس تایید شده"""
    def has_permission(self, request, view):
        return (request.user.is_authenticated and 
                request.user.role == 'instructor' and 
                request.user.is_instructor_approved)

class IsStudent(permissions.BasePermission):
    """دانشجو"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'student'

class CanCreateCourse(permissions.BasePermission):
    """می‌تواند دوره ایجاد کند (مدرس یا ادمین)"""
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return (request.user.role == 'instructor' and request.user.is_instructor_approved) or request.user.role == 'admin' or request.user.is_superuser