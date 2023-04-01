from django.urls import path, include
from rest_framework import routers

from users.views import FollowViewSet

app_name = 'users'

router_v1 = routers.DefaultRouter()
# router_v1.register('subscriptions/', ListFollowViewSet,
#                    basename='subscriptions')
router_v1.register(r'(?P<user_id>\d+)/subscribe/', FollowViewSet,
                   basename='subscribe')

urlpatterns = [
    path('', include(router_v1.urls)),
]
