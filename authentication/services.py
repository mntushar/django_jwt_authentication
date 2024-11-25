import uuid

from asgiref.sync import sync_to_async
from django.contrib.auth import authenticate

from Inventory import settings
from backend.account.authentication.models import LoginResponse, Login
from backend.account.user.models import User
from library.Utility.information import Information
from library.account.jwtHandler import JWTHandler
from library.account.tokenHandler import TokenHandler
from library.account.utility import Utility
from library.models.base_model_services import ModelServices


class AuthenticationService:
    token_handler = JWTHandler()
    utility = Utility()
    refresh_token_handler = TokenHandler()
    user_model_services = ModelServices(User)
    __public_key = settings.SETTING.JWT_PUBLIC_KEY

    def __init__(self):
        self.login_response = LoginResponse()

    async def login(self, login: Login) -> LoginResponse:
        try:
            user: User = await sync_to_async(authenticate)(username=login.username, password=login.password)
            if not user:
                self.login_response.is_success = False
                self.login_response.error = 'Invalid user or password'
                return self.login_response

            user_claim = await self.user_claim(user)

            self.login_response.access_token = self.token_handler.generate_token(user_claim)
            self.login_response.refresh_token = (self.refresh_token_handler
                                                 .generate_refresh_token(str(user.id)))
            self.login_response.public_key = self.__public_key

            return self.login_response
        except Exception as e:
            self.login_response.is_success = False
            self.login_response.error = self.utility.get_error(e)
            return self.login_response

    async def user_claim(self, user: User) -> dict:
        user_claim = {
            'id': str(user.id),
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_active': user.is_active,
            'is_superuser': user.is_superuser,
            'is_staff': user.is_staff,
        }

        user_claim = await self.user_permission(user, user_claim)

        return user_claim

    @sync_to_async
    def user_permission(self, user: User, claim: dict) -> dict:
        permission = [
            permission.codename
            for group in user.groups.all()
            for permission in group.permissions.all()
        ]
        claim[Information.jwt_token_permission_name] = permission

        return claim

    async def get_access_token(self, token: str) -> LoginResponse:
        try:
            user_id: str = self.refresh_token_handler.refresh_token_decode(token)

            if not user_id:
                self.login_response.is_success = False
                self.login_response.error = 'Invalid token'
                return self.login_response

            user = await self.user_model_services.get(uuid.UUID(user_id))

            if not user:
                self.login_response.is_success = False
                self.login_response.error = 'Invalid token'
                return self.login_response

            user_claim = await self.user_claim(user)
            self.login_response.access_token = self.token_handler.generate_token(user_claim)

            return self.login_response
        except Exception as e:
            self.login_response.is_success = False
            self.login_response.error = self.utility.get_error(e)
            return self.login_response
