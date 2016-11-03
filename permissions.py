from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS

from menu.models import Menu


class AnyCanReadButOnlySuperCanAdd(BasePermission):
    """
    根目录权限
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        else:
            return request.user.is_superuser


class AnyCanReadButOnlyOwnerCanUpdate(BasePermission):
    """
    子目录权限,只有拥有者才可以更改
    """
    message = "只有拥有者才能删除"

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        else:
            if hasattr(obj, 'owner'):
                return request.user == obj.owner
            elif hasattr(obj, 'create_person'):
                return request.user == obj.create_person
            else:
                raise AttributeError


class AnyCanReadButOnlyOwnerOrAdministratorCanAddChild(BasePermission):
    """
    子目录权限,只有管理员及拥有者才可以增加子目录
    """
    message = "只有管理员或拥有者才能增加子目录"

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        else:
            if hasattr(obj, 'owner'):
                return request.user == obj.owner
            elif hasattr(obj, 'administrators'):
                return obj.administrators.filter(pk=request.user.pk).exists()
            else:
                raise AttributeError


class OnlyOwnerCanOperate(BasePermission):
    """
    子目录管理权限，只有管理员才可以更改或删除
    """
    message = "只有管理员可以管理目录管理员"

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'owner'):
            return request.user == obj.owner
        elif hasattr(obj, 'create_person'):
            return request.user == obj.create_person
        else:
            raise AttributeError
