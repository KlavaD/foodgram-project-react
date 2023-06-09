from django.conf import settings
from rest_framework import serializers

from recipes.models import Recipe
from users.models import Follow, User
from users.validators import username_validator


class CustomUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=settings.FIELD_EMAIL_LENGTH)
    username = serializers.CharField(max_length=settings.NAMES_LENGTH,
                                     validators=[username_validator])
    first_name = serializers.CharField(max_length=settings.NAMES_LENGTH)
    last_name = serializers.CharField(max_length=settings.NAMES_LENGTH)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username',
            'first_name', 'last_name', 'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        return (request and request.user.is_authenticated
                and obj.author.filter(user=request.user).exists())


class ShortedRecipesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = (
            'id', 'name', 'image', 'cooking_time'
        )


class FollowSerializer(CustomUserSerializer):
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.ReadOnlyField(source='recipes.count')

    class Meta(CustomUserSerializer.Meta):
        fields = CustomUserSerializer.Meta.fields + (
            'recipes', 'recipes_count'
        )
        read_only_fields = ('recipes',)

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        return request and request.user.is_authenticated

    def get_recipes(self, obj):
        print('obj', obj)
        recipes_limit = self.context.get(
            'request').query_params.get('recipes_limit')
        data = obj.recipes.all()
        if recipes_limit:
            data = data[:int(recipes_limit)]
        return ShortedRecipesSerializer(data, many=True).data


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
        return FollowSerializer(
            instance, context={'request': self.context.get('request')}
        ).data
