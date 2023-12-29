from rest_framework import serializers

from Category.models import Category
from Item.models import Item


class ItemSerializer(serializers.HyperlinkedModelSerializer):
    category = serializers.SlugRelatedField("uuid", queryset=Category.objects.all())

    class Meta:
        model = Item
        fields = ('uuid', 'title', 'description', 'price', 'category')
        read_only_fields = ('uuid',)
