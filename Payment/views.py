from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from Payment.models import Payment, PAYMENT_STATUSES
from Payment.serializers import PaymentSerializer


class PaymentViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    serializer_class = PaymentSerializer

    def perform_create(self, serializer: PaymentSerializer):
        if not self.request.session or not self.request.session.session_key:
            self.request.session.save()
        serializer.save(session_key_id=self.request.session.session_key, status=PAYMENT_STATUSES.created)

    def get_queryset(self):
        payment_filter = (
            Payment.objects
            .filter(session_key=self.request.session.session_key)
            .exclude(status__in=(PAYMENT_STATUSES.created,))
        )
        return payment_filter.all()
