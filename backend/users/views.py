from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.models import Follow, User
from users.serializers import FollowSerializer, PostFollowSerializer


class UserViewSet(UserViewSet):

    @action(detail=False, methods=['GET'],
            permission_classes=[IsAuthenticated],
            serializer_class=FollowSerializer)
    def subscriptions(self, request):
        queryset = Follow.objects.filter(user=request.user)
        queryset = self.paginate_queryset(queryset)
        serializer = FollowSerializer(
            queryset, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(detail=False, url_path=r'(?P<user_id>\d+)/subscribe',
            permission_classes=[IsAuthenticated], methods=['POST', 'DELETE'],
            serializer_class=PostFollowSerializer)
    def subscribe(self, request, user_id):
        author = User.objects.get(id=user_id)
        user = self.request.user
        if request.method == 'POST':
            serializer = PostFollowSerializer(
                author, data=request.data, context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            Follow.objects.create(user=user, author=author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            Follow.objects.get(user=user, author=author).delete()
            return Response(request.data, status=status.HTTP_204_NO_CONTENT)

