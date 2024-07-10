import uuid
from django.db import models


class MicroServiceToken(models.Model):
    name = models.CharField(max_length=50)
    secret_key = models.UUIDField(default=uuid.uuid4, unique=True, db_index=True)
    description = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class OneTimeToken(models.Model):
    micro_service = models.ForeignKey(MicroServiceToken, on_delete=models.CASCADE)
    secret_token = models.UUIDField(default=uuid.uuid4)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.created_at)
