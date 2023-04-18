from operator import attrgetter

from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from recipes.models import (Tag, Ingredient, Recipe, ShoppingCart, Favorite,
                            ListOfIngredients)
from users.serializers import CustomUserSerializer, ShortedRecipesSerializer


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
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = ListOfIngredients
        fields = ('id', 'name', 'measurement_unit', 'amount')


class PostListOfIngredientsSerializer(serializers.ModelSerializer):
    id = serializers.SlugRelatedField(
        queryset=Ingredient.objects.all(),
        slug_field='id'
    )
    amount = serializers.IntegerField()

    class Meta:
        model = ListOfIngredients
        fields = ('id', 'amount')


class RecipesSerializer(serializers.ModelSerializer):
    tags = TagsSerializer(many=True,
                          read_only=True)
    ingredients = serializers.SerializerMethodField()
    author = CustomUserSerializer(read_only=True)
    image = Base64ImageField(required=False, allow_null=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    def get_ingredients(self, obj):
        return ListOfIngredientsSerializer(
            ListOfIngredients.objects.filter(recipe=obj),
            many=True
        ).data

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        user = request.user
        return (
                request and not user.is_anonymous
                and
                obj.favorite.filter(user=user).exists()
        )

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        user = request.user
        return (
                request and not user.is_anonymous
                and
                obj.shopping_cart.filter(user=user).exists()
        )

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients',
            "is_favorited", "is_in_shopping_cart",
            'name', 'image', 'text', 'cooking_time'
        )


class PostRecipesSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(
        many=True,
        queryset=Tag.objects.all(),
        slug_field='id'
    )
    ingredients = PostListOfIngredientsSerializer(many=True)
    image = Base64ImageField(required=False, allow_null=True)
    cooking_time = serializers.IntegerField(min_value=1)

    class Meta:
        model = Recipe
        fields = (
            'ingredients', 'tags', 'image', 'author',
            'name', 'image', 'text', 'cooking_time'
        )
        read_only_fields = ('author',)

    def create_ingredients_for_recipe(self, ingredients, recipe):
        list_of_ingredients = [
            ListOfIngredients(
                ingredient_id=ingredient.get('id').pk,
                amount=ingredient['amount'],
                recipe=recipe
            ) for ingredient in ingredients
        ]
        ListOfIngredients.objects.bulk_create(
            sorted(
                list_of_ingredients,
                key=attrgetter('ingredient.name')
            )
        )

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data,
                                       author=self.context['request'].user)
        self.create_ingredients_for_recipe(ingredients, recipe)
        recipe.tags.set(tags)
        return recipe

    def update(self, instance, validated_data):
        if instance.author != self.context['request'].user:
            raise ValidationError('Исправлять может только автор')
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        super().update(instance, validated_data)
        ListOfIngredients.objects.filter(
            recipe=instance
        ).delete()
        self.create_ingredients_for_recipe(ingredients, instance)
        instance.tags.set(tags)
        instance.save()
        return instance

    def validate(self, data):
        ingredients = self.initial_data.get('ingredients')
        tags = self.initial_data.get('tags')
        list_ingredients_id = []
        for ingredient in ingredients:
            if int(ingredient['amount']) < 1:
                raise ValidationError('Количество должно быть больше 1')
            if ingredient['id'] in list_ingredients_id:
                raise ValidationError('Ингредиенты не уникальны')
            list_ingredients_id.append(ingredient['id'])
        for tag in tags:
            if tags.count(tag) > 1:
                raise ValidationError('Тэги не уникальны')
        return data

    def to_representation(self, instance):
        return RecipesSerializer(
            instance,
            context={'request': self.context.get('request')}
        ).data


class ShoppingCartSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('user', 'recipe')
        model = ShoppingCart
        read_only_fields = ('recipe', 'user')

    def validate(self, data):
        recipe = self.initial_data.get('recipe')
        user = self.initial_data.get('user')
        if self.Meta.model.objects.filter(user=user, recipe=recipe).exists():
            raise serializers.ValidationError(
                'Уже добавлено!')
        return data

    def to_representation(self, instance):
        return ShortedRecipesSerializer(
            instance.recipe,
            context={'recipe': self.initial_data.get('recipe')}
        ).data


class FavoriteSerializer(ShoppingCartSerializer):
    class Meta(ShoppingCartSerializer.Meta):
        model = Favorite
