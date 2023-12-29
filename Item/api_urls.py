from rest_framework.routers import SimpleRouter

from Item.views import ItemViewSet

router = SimpleRouter()

router.register("", ItemViewSet)

urlpatterns = router.urls
