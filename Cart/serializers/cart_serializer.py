from rest_framework import serializers

from Cart.models import Cart
from Item.models import Item


class CartSerializer(serializers.HyperlinkedModelSerializer):
    item = serializers.SlugRelatedField("uuid", queryset=Item.objects.all())

    class Meta:
        model = Cart
        fields = ('uuid', 'item', 'count')
        read_only_fields = ('uuid', )
