from django.db.models import Count
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from backend.settings import FIELD_EMAIL_LENGTH, NAMES_LENGTH
from users.models import User, Follow
from users.validators import username_validator


class SelfValidator(object):
    requires_context = True

    def __call__(self, value, serializer_field):
        if value == serializer_field.context['request'].user:
            raise serializers.ValidationError(
                'You cannot follow yourself!')
        return value


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=FIELD_EMAIL_LENGTH)
    username = serializers.CharField(max_length=NAMES_LENGTH,
                                     validators=[username_validator])
    first_name = serializers.CharField(max_length=NAMES_LENGTH)
    last_name = serializers.CharField(max_length=NAMES_LENGTH)
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request is not None and hasattr(request, "user"):
            user = self.context['request'].user
            if user.is_anonymous:
                return False
            if Follow.objects.filter(user=user,
                                     author=obj.id).exists():
                return True
            return False

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )


from api.serializers import RecipesSerializer


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault())

    author = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
        validators=[SelfValidator()])

    recipes = RecipesSerializer(many=True, required=False)

    recipe_count = serializers.SerializerMethodField()

    def get_recipes_count(self, obj):
        return obj.author.resipes.count()

    class Meta:
        model = Follow
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['user', 'author'],
                message='you are already follow this author!'
            )
        ]
