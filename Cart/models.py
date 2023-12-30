from uuid import uuid4

from django.contrib.sessions.models import Session
from django.core.validators import MinValueValidator
from django.db import models

from Item.models import Item


class Cart(models.Model):
    uuid = models.UUIDField(primary_key=True, unique=True, default=uuid4)

    session_key = models.ForeignKey(Session, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    count = models.IntegerField(validators=[MinValueValidator(1, "Count cannot be negative or zero")])

    def __str__(self):
        return f"{self.item} : {self.count}"
