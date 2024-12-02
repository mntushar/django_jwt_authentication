from rest_framework.authentication import BasicAuthentication
from rest_framework.exceptions import AuthenticationFailed

from library.Utility.utility import Utility
from library.account.utility import Utility as account_utility
from library.account.jwtHandler import JWTHandler
from library.models.response import Response


class JwtLoginRequiredMixin(BasicAuthentication):
    __jwt_handler = JWTHandler()
    __utility = Utility()
    __account_utility = account_utility()
    __response = Response()

    def authenticate(self, request):
        token = self.__account_utility.get_token(request)

        data = self.__jwt_handler.verify_token(token)
        if not data.is_success:
            raise AuthenticationFailed(self.__utility.get_error(data.message))

        user = {
            'id': data.message['id'],
            'username': data.message['username'],
            'email': data.message['email'],
        }

        return (user, None)


