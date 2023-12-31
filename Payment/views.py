from uuid import UUID

import stripe as stripe
from django.conf import settings
from django.http import HttpRequest
from django.shortcuts import render
from django.views import View
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from Payment.models import Payment, PAYMENT_STATUSES
from Payment.serializers import PaymentSerializer
from Payment.tasks import create_payment_intent


class PaymentViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    serializer_class = PaymentSerializer

    def perform_create(self, serializer: PaymentSerializer):
        if not self.request.session or not self.request.session.session_key:
            self.request.session.save()
        payment = serializer.save(session_key_id=self.request.session.session_key, status=PAYMENT_STATUSES.created)
        create_payment_intent.delay(payment.uuid)

    def get_queryset(self):
        payment_filter = (
            Payment.objects
            .filter(session_key=self.request.session.session_key)
            .exclude(status__in=(PAYMENT_STATUSES.created,))
        )
        return payment_filter.all()


class PaymentView(View):
    def get(self, request: HttpRequest, uuid: UUID):
        payment = Payment.objects.get(uuid=uuid)
        if payment.status == PAYMENT_STATUSES.created:
            return render(request, "waiting_for_payment.html")
        if payment.status == PAYMENT_STATUSES.success:
            return self.__handle_success(request)
        stripe.api_key = settings.STRIPE_API_KEY
        intent = stripe.PaymentIntent.retrieve(payment.client_secret.split("_secret_")[0])
        if intent["status"] == "succeeded":
            payment.status = PAYMENT_STATUSES.success
            payment.save()
            return self.__handle_success(request)
        if intent["status"] == "canceled":
            payment.status = PAYMENT_STATUSES.canceled
            payment.save()
            return self.__handle_canceled(request, payment)

        return self.__handle_waiting(request, payment)

    def __handle_waiting(self, request: HttpRequest, payment: Payment):
        return render(
            request,
            "payment.html",
            {
                "DOMAIN": settings.STRIPE_BACK_URL,
                "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY,
                "payment": payment
            }
        )

    def __handle_success(self, request: HttpRequest):
        return render(request, "successful_payment.html")

    def __handle_canceled(self, request: HttpRequest, payment: Payment):
        payment.status = PAYMENT_STATUSES.waiting
        payment.save()
        return render(
            request,
            "payment.html",
            {
                "canceled": True,
                "DOMAIN": settings.STRIPE_BACK_URL,
                "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY,
                "payment": payment
            }
        )
