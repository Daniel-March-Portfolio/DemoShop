from uuid import uuid4

from django.db import models


class Category(models.Model):
    uuid = models.UUIDField(primary_key=True, unique=True, default=uuid4)

    title = models.CharField(max_length=60, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Categories"
