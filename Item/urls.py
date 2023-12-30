from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('<uuid:uuid>', TemplateView.as_view(template_name="item.html"))
]
