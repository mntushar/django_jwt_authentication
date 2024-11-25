from library.models.response import Response
from django.db import models


class Login(models.Model):
    username = models.CharField()
    password = models.CharField()

    class Meta:
        managed = False


class LoginResponse(Response):
    def __init__(self):
        super().__init__()
        self.access_token = None
        self.refresh_token = None
        self.public_key = None

    def to_dict(self):
        return vars(self)