from http import HTTPStatus

from django.db.models import Count
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework.decorators import action

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.models import Follow, User
from users.serializers import PostFollowSerializer, FollowSerializer


class UserViewSet(UserViewSet):

    @action(detail=False, methods=['GET'],
            url_path='subscriptions',
            permission_classes=[IsAuthenticated],
            serializer_class=FollowSerializer)
    def subscriptions(self, request):
        following = Follow.objects.filter(user=request.user).annotate(
            recipes_count=Count('author__recipes'))
        serializer = self.get_serializer(following, many=True)
        return Response(serializer.data)
        # return self.request.user.follower.all()

    @action(detail=False, methods=['POST'],
            url_path=r'(?P<user_id>\d+)/subscribe',
            permission_classes=[IsAuthenticated],
            serializer_class=PostFollowSerializer
            )
    def subscribe(self, request, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, author=kwargs.get('user_id'))
        return Response(serializer.data,  status=HTTPStatus.OK)

