from datetime import datetime, timedelta

from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed

from library.Utility.cryptography import AesCryptography


class TokenHandler:
    __refresh_token_password = settings.SETTING.Refresh_token_password
    __refresh_token_validation = int(settings.SETTING.Refresh_TOKEN_VALIDATION_TIME)
    __aes_cryptography = AesCryptography()
    __string_separator = ';'

    def generate_refresh_token(self, user_id: str) -> str:
        date = str(int((datetime.now() + timedelta(seconds=self.__refresh_token_validation)).timestamp()))
        data = self.__string_separator.join([
            f"{user_id}",
            f"{date}"
        ])
        encrypt = self.__aes_cryptography.encrypt(data, self.__refresh_token_password)
        return encrypt

    def refresh_token_decode(self, token: str) -> str:
        try:
            data = self.__aes_cryptography.decrypt(token, self.__refresh_token_password)
            data_list = data.split(self.__string_separator)
            expired_date = data_list[1]
            timestamp = int(expired_date)
            expired_date_obj = datetime.fromtimestamp(timestamp)

            if expired_date_obj < datetime.now():
                raise AuthenticationFailed('Token expired')
            return data_list[0]
        except Exception as e:
            raise e

