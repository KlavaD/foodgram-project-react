from django.contrib.auth import get_user_model
from rest_framework.routers import DefaultRouter

from users.views import UserViewSet

router = DefaultRouter()
router.register("users", UserViewSet)

User = get_user_model()

urlpatterns = router.urls
