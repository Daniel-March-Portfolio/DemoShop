from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet

from Category.models import Category
from Category.serializers import CategorySerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    permission_classes = [
        permissions.DjangoModelPermissionsOrAnonReadOnly
    ]
