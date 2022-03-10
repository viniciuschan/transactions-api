from rest_framework import routers

from .views import TransactionViewSet

router = routers.DefaultRouter()
router.register(
    r"transactions",
    TransactionViewSet,
    basename="transactions",
)

urlpatterns = router.urls
