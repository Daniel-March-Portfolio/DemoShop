from rest_framework.routers import SimpleRouter

from Cart.views import CartViewSet

router = SimpleRouter()

router.register("", CartViewSet, basename="Cart")

urlpatterns = router.urls
