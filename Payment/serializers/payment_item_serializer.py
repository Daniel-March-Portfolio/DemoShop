from rest_framework import serializers

from Item.models import Item
from Payment.models import PaymentItem


class PaymentItemSerializer(serializers.HyperlinkedModelSerializer):
    item = serializers.SlugRelatedField("uuid", queryset=Item.objects.all())

    class Meta:
        model = PaymentItem
        fields = ('uuid', 'item', 'count')
        read_only_fields = ('uuid',)
