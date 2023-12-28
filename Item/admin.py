from django.contrib import admin

from Item.models import Item


class ItemAdmin(admin.ModelAdmin):
    readonly_fields = ("uuid",)


admin.site.register(Item, ItemAdmin)
