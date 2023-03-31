from rest_framework import viewsets
from rest_framework.mixins import ListModelMixin, CreateModelMixin, \
    DestroyModelMixin

from users.serializers import FollowSerializer


class ListFollowViewSet(ListModelMixin, viewsets.GenericViewSet):
    serializer_class = FollowSerializer

    def get_queryset(self):
        return self.request.user.follower.all()


class FollowViewSet(CreateModelMixin, DestroyModelMixin,
                    viewsets.GenericViewSet):
    serializer_class = FollowSerializer

    def get_queryset(self):
        return self.request.user.follower.all()
