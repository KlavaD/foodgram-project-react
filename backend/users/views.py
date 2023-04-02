from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.models import Follow, User
from users.serializers import PostFollowSerializer, FollowSerializer


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.annotate(recipes_count=Count('author__recipes'))
    permission_classes = (IsAuthenticated,)
    serializer_class = PostFollowSerializer

    @action(detail=False, url_path='subscriptions',
            methods=['GET'])
    def get_queryset(self, request):
        # following = Follow.objects.filter(user=request.user)
        # serializer = self.get_serializer(following, many=True)
        # return Response(serializer.data)
        return self.request.user.follower.all()

    def get_serializer_class(self):
        if self.action in ['create', 'delete']:
            return PostFollowSerializer
        return FollowSerializer

    def get_author(self):
        return get_object_or_404(User, pk=self.kwargs.get('user_id'))

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, author=self.get_author())
