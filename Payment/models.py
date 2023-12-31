from dataclasses import dataclass
from uuid import uuid4

from django.contrib.sessions.models import Session
from django.core.validators import MinValueValidator
from django.db import models

from Item.models import Item


@dataclass
class PAYMENT_STATUSES:
    created = "created"
    waiting = "waiting"
    success = "success"
    canceled = "canceled"


class Payment(models.Model):
    _STATUSES = {
        (PAYMENT_STATUSES.created, "Created"),
        (PAYMENT_STATUSES.waiting, "Waiting for payment"),
        (PAYMENT_STATUSES.success, "Success"),
        (PAYMENT_STATUSES.canceled, "Canceled"),
    }

    uuid = models.UUIDField(primary_key=True, unique=True, default=uuid4)

    client_secret = models.CharField(max_length=120)
    session_key = models.ForeignKey(Session, on_delete=models.CASCADE)
    status = models.CharField(max_length=60, choices=_STATUSES)

    def __str__(self):
        return self.uuid


class PaymentItem(models.Model):
    uuid = models.UUIDField(primary_key=True, unique=True, default=uuid4)

    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, )
    count = models.IntegerField(validators=[MinValueValidator(1, "Count cannot be negative or zero")])

    def __str__(self):
        return f"{self.item} : {self.count}"
