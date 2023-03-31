import base64

from django.contrib.auth.models import AnonymousUser
from django.shortcuts import get_object_or_404
from django.core.files.base import ContentFile
from rest_framework import serializers

from recipes.models import (Tag, Ingredient, Recipe, ShoppingCart, Favorite,
                            ListOfIngredients, TagsRecipes)
from users.serializers import UserSerializer


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class ListOfIngredientsSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = ListOfIngredients
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipesSerializer(serializers.ModelSerializer):
    tags = TagsSerializer(many=True,
                          read_only=True)
    ingredients = ListOfIngredientsSerializer(
        many=True,
        read_only=True,
        source='recipe_ingredients'
    )
    author = UserSerializer(read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request is not None and hasattr(request, "user"):
            user = self.context['request'].user
            if user.is_anonymous:
                return False
            if Favorite.objects.filter(user=user,
                                       recipe=obj.id).exists():
                return True
            return False

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request is not None and hasattr(request, "user"):
            user = self.context['request'].user
            if user.is_anonymous:
                return False
            if get_object_or_404(ShoppingCart, user=user,
                                 recipe=obj.id):
                return True
            return False

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients',
            "is_favorited", "is_in_shopping_cart",
            'name', 'image', 'text', 'cooking_time'
        )
        read_only_fields = (
            'id', 'tags', 'author', 'ingredients',
            'name', 'image', 'text', 'cooking_time'
        )


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class PostRecipesSerializer(serializers.ModelSerializer):
    tags = TagsSerializer(many=True, source='tags.id')
    ingredients = ListOfIngredientsSerializer(many=True)
    image = Base64ImageField(required=False, allow_null=True)
    cooking_time = serializers.IntegerField(min_value=1)

    class Meta:
        model = Recipe
        fields = (
            'ingredients', 'tags', 'image', 'author',
            'name', 'image', 'text', 'cooking_time'
        )
        read_only_fields = ('author',)

    def create(self, validated_data):
        print(validated_data)
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')

        recipe = Recipe.objects.create(**validated_data)
        for tag in tags:
            TagsRecipes.objects.create(tags=tag,
                                       recipe=recipe)
        for ingredient in ingredients:
            ListOfIngredients.objects.create(**ingredient,
                                             recipe=recipe)
        return recipe

    def to_representation(self, instance):
        return RecipesSerializer(instance)


class ShoppingCartSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = ShoppingCart
        read_only_fields = ('recipe',)


class FavoriteSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Favorite
        read_only_fields = ('recipe',)
