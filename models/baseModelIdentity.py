from django.db import models
from django.conf import settings

from library.models.baseModel import BaseModel


class BaseModelIdentity(BaseModel):
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="%(class)s_created_by")
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="%(class)s_modified_by")
    deleted_at = models.DateTimeField(null=True)
    deleted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="%(class)s_deleted_by")

    class Meta:
        abstract = True