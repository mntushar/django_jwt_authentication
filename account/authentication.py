from rest_framework.authentication import BasicAuthentication
from rest_framework.exceptions import AuthenticationFailed

from library.account.jwtHandler import JWTHandler
from library.account.utility import Utility
from library.models.response import Response


class JwtLoginRequiredMixin(BasicAuthentication):
    __jwt_handler = JWTHandler()
    __utility = Utility()
    __response = Response()

    def authenticate(self, request):
        token = self.__utility.get_token(request)

        valid_token = self.__jwt_handler.verify_token(token)
        if not valid_token:
            raise AuthenticationFailed()

        user = {
            'id': valid_token['id'],
            'username': valid_token['username'],
            'email': valid_token['email'],
        }

        return (user, None)


