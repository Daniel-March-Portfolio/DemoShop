from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name="categories.html")),
    path('<uuid:uuid>', TemplateView.as_view(template_name="category.html"))
]
