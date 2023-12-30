from django.contrib import admin

from Cart.models import Cart


class CartAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


admin.site.register(Cart, CartAdmin)
