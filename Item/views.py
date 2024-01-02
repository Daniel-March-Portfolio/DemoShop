from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from rest_framework.viewsets import ReadOnlyModelViewSet

from Item.models import Item
from Item.serializers import ItemSerializer


class ItemViewSet(ReadOnlyModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    permission_classes = [
        permissions.DjangoModelPermissionsOrAnonReadOnly
    ]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["category"]
