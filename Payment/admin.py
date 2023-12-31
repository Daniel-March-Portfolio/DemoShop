from django.contrib import admin

from Payment.models import Payment, PaymentItem


class PaymentAdmin(admin.ModelAdmin):
    def has_change_permission(self, request, obj=None):
        return False


class PaymentItemAdmin(admin.ModelAdmin):
    def has_change_permission(self, request, obj=None):
        return False


admin.site.register(Payment, PaymentAdmin)
admin.site.register(PaymentItem, PaymentItemAdmin)
