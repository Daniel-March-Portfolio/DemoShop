from django.http import HttpRequest
from django.views import View
from rest_framework.permissions import BasePermission
from rest_framework.viewsets import ModelViewSet

from Cart.models import Cart
from Cart.serializers import CartSerializer


class IsOwner(BasePermission):
    def has_object_permission(self, request: HttpRequest, view: View, obj: Cart) -> bool:
        return obj.session_key.session_key == request.session.session_key


class CartViewSet(ModelViewSet):
    serializer_class = CartSerializer

    permission_classes = [
        IsOwner,
    ]

    def get_queryset(self):
        return Cart.objects.filter(session_key=self.request.session.session_key).all()

    def perform_create(self, serializer: CartSerializer):
        if not self.request.session or not self.request.session.session_key:
            self.request.session.save()
        Cart.objects.filter(
            session_key_id=self.request.session.session_key,
            item_id=serializer.validated_data["item"]
        ).delete()
        serializer.save(session_key_id=self.request.session.session_key)
