from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from backend.settings import FIELD_EMAIL_LENGTH, NAMES_LENGTH
from recipes.models import Recipe
from users.models import User, Follow
from users.validators import username_validator


class SelfValidator(object):
    requires_context = True

    def __call__(self, value, serializer_field):
        if value == serializer_field.context['request'].user:
            raise serializers.ValidationError(
                'You cannot follow yourself!')
        return value


class CustomUserSerializer(serializers.ModelSerializer):
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
            return Follow.objects.filter(user=user,
                                         author=obj.id).exists()

    class Meta:
        model = User
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name', 'is_subscribed'
                  )


from api.serializers import RecipesSerializer, ShortedRecipesSerializer


class FollowSerializer(CustomUserSerializer):
    email = serializers.ReadOnlyField(source='author.email')
    id = serializers.ReadOnlyField(source='author.id')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request is not None and hasattr(request, "user"):
            user = self.context['request'].user
            if user.is_anonymous:
                return False
            return Follow.objects.filter(user=user,
                                         author=obj.id).exists()

    recipes = serializers.SerializerMethodField()
    # recipes = ShortedRecipesSerializer(many=True,
    #                                    read_only=True,
    #                                    source='author.recipes.all',
    #                                    )
    recipes_count = serializers.SerializerMethodField()

    class Meta(CustomUserSerializer.Meta):
        fields = CustomUserSerializer.Meta.fields + ('recipes', 'recipes_count')
        read_only_fields = ('recipes',)

    def get_recipes(self, obj):
        # recipes_limit = self.context['recipes_limit']
        data = Recipe.objects.filter(author=obj.author)[:3]
        return ShortedRecipesSerializer(data)

    def get_recipes_count(self, obj):
        return obj.author.recipes.count()


class PostFollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault())

    class Meta:
        fields = '__all__'
        model = Follow
        read_only_fields = ('author',)
        # validators = [
        #     UniqueTogetherValidator(
        #         queryset=Follow.objects.all(),
        #         fields=['author', 'user'],
        #         message='you are already follow this author!'
        #     )
        # ]

    # def validate(self, data):
    #     author = self.context.get('request').user.id
    #     user = self.context['request'].user
    #     if Follow.objects.filter(author=author, user=user).exists():
    #         raise serializers.ValidationError(
    #             'Нельзя подписаться на самого себя')
    #     return data

    # def to_representation(self, instance):
    #     return FollowSerializer(instance)
