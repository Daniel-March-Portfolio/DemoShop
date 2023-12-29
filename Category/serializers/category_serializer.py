from rest_framework import serializers

from Category.models import Category


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ('uuid', 'title')
        read_only_fields = ('uuid',)
