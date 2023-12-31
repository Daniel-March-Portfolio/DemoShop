from rest_framework import serializers

from Payment.models import Payment, PaymentItem
from Payment.serializers import PaymentItemSerializer


class PaymentSerializer(serializers.HyperlinkedModelSerializer):
    items = PaymentItemSerializer(source="paymentitem_set", many=True)

    class Meta:
        model = Payment
        fields = ('uuid', 'client_secret', 'status', "items")
        read_only_fields = ('uuid', 'client_secret', 'status')

    def create(self, validated_data):
        payment_items_data = validated_data.pop('paymentitem_set')
        payment = Payment.objects.create(**validated_data)

        for payment_item in payment_items_data:
            PaymentItem.objects.create(payment=payment, **payment_item)

        return payment
