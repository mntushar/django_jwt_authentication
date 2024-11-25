from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission

from library.Utility.information import Information
from library.account.jwtHandler import JWTHandler
from library.account.utility import Utility


class JwtAuthorization(BasePermission):
    __jwt_handler = JWTHandler()
    __utility = Utility()


    def has_permission(self, request, view):
        perms = view.permission_required

        token = self.__utility.get_token(request)

        payload = self.__jwt_handler.decode_token(token)

        permissions = payload.get(Information.jwt_token_permission_name, {})

        if isinstance(perms, str):
            if not perms in permissions:
                raise PermissionDenied("Permission is denied.")

        elif isinstance(perms, list):
            has_permission = any(map(lambda perm: perm in permissions, perms))
            if not has_permission:
                raise PermissionDenied("Permission is denied.")

        return True