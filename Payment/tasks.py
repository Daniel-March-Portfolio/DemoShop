from uuid import UUID

import stripe
from celery import shared_task
from django.conf import settings

from Payment.models import Payment, PaymentItem, PAYMENT_STATUSES


@shared_task
def create_payment_intent(payment_uuid: UUID):
    payment = Payment.objects.get(uuid=payment_uuid)
    stripe.api_key = settings.STRIPE_API_KEY
    payment_items: list[PaymentItem] = payment.paymentitem_set.all()
    payment_intent = stripe.PaymentIntent.create(
        amount=int(sum((payment_item.item.price * payment_item.count for payment_item in payment_items))*100),
        currency="USD"
    )
    payment.client_secret = payment_intent["client_secret"]
    payment.status = PAYMENT_STATUSES.waiting
    payment.save()


@shared_task
def create_payment_intents():
    created_payments = Payment.objects.filter(status=PAYMENT_STATUSES.created).all()
    for created_payment in created_payments:
        create_payment_intent.delay(created_payment.uuid)
