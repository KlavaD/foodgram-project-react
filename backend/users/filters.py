from django_filters import rest_framework as filters

from users.models import Follow


class FollowFilter(filters.FilterSet):
    user = filters.CharFilter(field_name='user__id')

    class Meta:
        model = Follow
        fields = (
            'user',
        )
