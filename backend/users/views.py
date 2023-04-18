from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.models import Follow, User
from users.serializers import FollowSerializer, PostFollowSerializer


class UserViewSet(UserViewSet):

    @action(detail=False, methods=['GET'],
            permission_classes=[IsAuthenticated, ],
            pagination_class=LimitOffsetPagination
            )
    def subscriptions(self, request):
        queryset = Follow.objects.filter(user=self.request.user)
        queryset = self.paginate_queryset(queryset)
        serializer = FollowSerializer(
            queryset, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(detail=False, url_path=r'(?P<user_id>\d+)/subscribe',
            permission_classes=[IsAuthenticated], methods=['POST', 'DELETE'],
            serializer_class=PostFollowSerializer)
    def subscribe(self, request, user_id):
        author = get_object_or_404(User, id=user_id)
        user = self.request.user
        data = {'user': user,
                'author': author
                }
        if request.method == 'POST':
            serializer = PostFollowSerializer(
                data=data, context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(user=user,
                            author=author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            get_object_or_404(Follow, user=user, author=author).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
