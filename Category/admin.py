from django.contrib import admin

from Category.models import Category


class CategoryAdmin(admin.ModelAdmin):
    readonly_fields = ("uuid",)


admin.site.register(Category, CategoryAdmin)
