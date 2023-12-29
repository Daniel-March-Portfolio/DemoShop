from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet

from Item.models import Item
from Item.serializers import ItemSerializer


class ItemViewSet(ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    permission_classes = [
        permissions.DjangoModelPermissionsOrAnonReadOnly
    ]
