from django.db import models
from django.conf import settings

from library.models.baseModelIdentity import BaseModelIdentity


class BaseModelClient(BaseModelIdentity):
    client_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="%(class)s_created_by")

    class Meta:
        abstract = True