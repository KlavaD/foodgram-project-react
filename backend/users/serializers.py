from rest_framework import serializers, pagination
from rest_framework.response import Response

from backend.settings import FIELD_EMAIL_LENGTH, NAMES_LENGTH
from recipes.models import Recipe
from users.models import User, Follow
from users.validators import username_validator


class CustomUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=FIELD_EMAIL_LENGTH)
    username = serializers.CharField(max_length=NAMES_LENGTH,
                                     validators=[username_validator])
    first_name = serializers.CharField(max_length=NAMES_LENGTH)
    last_name = serializers.CharField(max_length=NAMES_LENGTH)
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request is not None:
            user = request.user
            if user.is_anonymous:
                return False
            if Follow.objects.filter(user=user,
                                     author=obj.id).exists():
                return True
            return False

    class Meta:
        model = User
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name', 'is_subscribed'
                  )


from api.serializers import ShortedRecipesSerializer


class FollowSerializer(CustomUserSerializer):
    email = serializers.ReadOnlyField(source='author.email')
    id = serializers.ReadOnlyField(source='author.id')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request is not None:
            user = request.user
            if user.is_anonymous:
                return False
            if Follow.objects.filter(user=user,
                                     author=obj.author).exists():
                return True
            return False

    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta(CustomUserSerializer.Meta):
        fields = CustomUserSerializer.Meta.fields + ('recipes', 'recipes_count')
        read_only_fields = ('recipes',)

    def get_recipes(self, obj):
        paginator = pagination.PageNumberPagination()
        paginator.page_size = self.context.get(
            'request').query_params.get('recipes_limit')

        data = Recipe.objects.filter(author=obj.author)
        if not data:
            return None
        page = paginator.paginate_queryset(data, self.context.get('request'))
        return ShortedRecipesSerializer(page, many=True).data

    def get_recipes_count(self, obj):
        return obj.author.recipes.count()


class PostFollowSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('author', 'user')
        model = Follow
        read_only_fields = ('author', 'user')

    def validate(self, data):
        author = self.initial_data.get('author')
        user = self.context.get('request').user
        if Follow.objects.filter(author=author, user=user).exists():
            raise serializers.ValidationError(
                'Нельзя подписаться второй раз')
        if author == user:
            raise serializers.ValidationError(
                'Нельзя подписаться самого себя')
        return data

    def to_representation(self, instance):
        return FollowSerializer(instance,
                                context={
                                    'request': self.context.get('request')}
                                ).data
