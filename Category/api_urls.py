from rest_framework.routers import SimpleRouter

from Category.views import CategoryViewSet

router = SimpleRouter()

router.register("", CategoryViewSet)

urlpatterns = router.urls
