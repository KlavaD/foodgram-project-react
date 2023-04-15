import base64

from django.core.files.base import ContentFile
from rest_framework import serializers

from recipes.models import (Tag, Ingredient, Recipe, ShoppingCart, Favorite,
                            ListOfIngredients)
from users.serializers import CustomUserSerializer


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
    name = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )
    measurement_unit = serializers.SlugRelatedField(
        read_only=True,
        slug_field='measurement_unit'
    )

    class Meta:
        model = ListOfIngredients
        fields = ('id', 'name', 'measurement_unit', 'amount')


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class RecipesSerializer(serializers.ModelSerializer):
    tags = TagsSerializer(many=True,
                          read_only=True)
    ingredients = serializers.SerializerMethodField()
    author = CustomUserSerializer(read_only=True)
    image = Base64ImageField(required=False, allow_null=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    def get_ingredients(self, obj):
        data = ListOfIngredients.objects.filter(recipe=obj)
        if not data:
            return None
        return ListOfIngredientsSerializer(data, many=True).data

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request is not None:
            user = self.context['request'].user
            if user.is_anonymous:
                return False
            if Favorite.objects.filter(user=user,
                                       recipe=obj).exists():
                return True
        return False

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request is not None:
            user = self.context['request'].user
            if user.is_anonymous:
                return False
            if ShoppingCart.objects.filter(user=user,
                                           recipe=obj.id).exists():
                return True
        return False

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients',
            "is_favorited", "is_in_shopping_cart",
            'name', 'image', 'text', 'cooking_time'
        )


class ShortedRecipesSerializer(RecipesSerializer):
    class Meta:
        model = Recipe
        fields = (
            'id', 'name', 'image', 'cooking_time'
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
        for ingredient in ingredients:
            if ListOfIngredients.objects.filter(
                    ingredient_id=ingredient.get('id').pk,
                    recipe=recipe).exists():
                our_ingredient = ListOfIngredients.objects.get(
                    ingredient_id=ingredient.get('id').pk,
                    recipe=recipe)
                amount = our_ingredient.amount
                amount += ingredient['amount']
                our_ingredient.amount = amount
                our_ingredient.save()
            else:
                ListOfIngredients.objects.create(
                    ingredient_id=ingredient.get('id').pk,
                    amount=ingredient['amount'],
                    recipe=recipe
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
            raise serializers.ValidationError
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        instance.name = validated_data.get('name')
        instance.image = validated_data.get('image', instance.image)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get('cooking_time',
                                                   instance.cooking_time)
        ListOfIngredients.objects.filter(
            recipe=instance
        ).delete()
        self.create_ingredients_for_recipe(ingredients, instance)
        instance.tags.set(tags)
        instance.save()
        return instance

    def to_representation(self, instance):
        return RecipesSerializer(
            instance,
            context={'request': self.context.get('request')}
        ).data


class ShoppingCartSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='recipe.name')
    image = Base64ImageField(required=False, allow_null=True)
    cooking_time = serializers.ReadOnlyField(source='recipe.cooking_time')

    class Meta:
        fields = ('id', 'name', 'image', 'cooking_time')
        model = ShoppingCart
        read_only_fields = ('recipe',)

    def validate(self, data):
        recipe = self.initial_data.get('recipe')
        user = self.initial_data.get('user')
        if self.Meta.model.objects.filter(user=user, recipe=recipe).exists():
            raise serializers.ValidationError(
                'Уже добавлено!')
        return data


class FavoriteSerializer(ShoppingCartSerializer):
    class Meta(ShoppingCartSerializer.Meta):
        model = Favorite
