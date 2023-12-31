from django.urls import path
from django.views.generic import TemplateView

from Payment.views import PaymentView

urlpatterns = [
    path('', TemplateView.as_view(template_name="payments.html")),
    path('<uuid:uuid>', PaymentView.as_view())
]
