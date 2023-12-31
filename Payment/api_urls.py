from rest_framework.routers import SimpleRouter

from Payment.views import PaymentViewSet

router = SimpleRouter()

router.register("", PaymentViewSet, basename="Payment")

urlpatterns = router.urls
