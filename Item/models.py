from uuid import uuid4

from django.core.validators import MinValueValidator
from django.db import models

from Category.models import Category


class Item(models.Model):
    uuid = models.UUIDField(primary_key=True, unique=True, default=uuid4)

    title = models.CharField(max_length=60)
    description = models.TextField(max_length=800)
    price = models.FloatField(validators=[MinValueValidator(0, "Price cannot be negative")])

    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} ({self.category})"

    def save(
            self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.price = round(self.price, 2)
        super().save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields
        )
