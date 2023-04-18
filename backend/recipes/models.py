from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import UniqueConstraint

from users.models import User


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Имя тэга',
        unique=True,
        max_length=settings.FIELD_TEXT_LENGTH
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        unique=True,
        max_length=settings.FIELD_TEXT_LENGTH,
    )
    color = models.CharField(
        verbose_name='Цвет',
        unique=True,
        max_length=settings.FIELD_COLOR_LENGTH
    )

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
        ordering = ('name',)

    def __str__(self) -> str:
        return self.slug


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='Наименование ингредиента',
        max_length=settings.FIELD_TEXT_LENGTH
    )
    measurement_unit = models.CharField(
        verbose_name='Единица измерения',
        max_length=settings.FIELD_TEXT_LENGTH
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name',)
        constraints = [
            UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='double_ingredient'
            )
        ]

    def __str__(self) -> str:
        return f'{self.name}, {self.measurement_unit}'


class Recipe(models.Model):
    tags = models.ManyToManyField(
        Tag,
        blank=False,
        through='TagsRecipes',
        verbose_name='Тэги',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    name = models.CharField(
        max_length=settings.FIELD_TEXT_LENGTH,
        blank=False,
        null=False,
        verbose_name='Название'
    )
    image = models.ImageField(
        verbose_name='Фото',
        upload_to='recipe/images/',
        blank=True
    )
    text = models.CharField(
        max_length=settings.FIELD_TEXT_LENGTH,
        blank=False,
        null=False,
        verbose_name='Описание рецепта'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='ListOfIngredients',
        verbose_name='Ингредиенты',
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        blank=False,
        null=False,
        validators=[MinValueValidator(1)]
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.name[:15]


class ListOfIngredients(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        verbose_name='Наименование ингредиента',
        related_name='recipe_ingredients'
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        blank=False,
        null=False,
        validators=[MinValueValidator(1)]
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='recipe_ingredients',
    )

    class Meta:
        ordering = ('ingredient__name',)
        verbose_name = 'Список Ингредиентов'
        verbose_name_plural = 'Списки Ингредиентов'

    def __str__(self) -> str:
        return (f'({self.ingredient.name}-{self.amount}'
                f'({self.ingredient.measurement_unit})')


class TagsRecipes(models.Model):
    tags = models.ForeignKey(
        Tag,
        blank=False,
        null=False,
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Рецепт:Тэги'
        verbose_name_plural = 'Рецепты:Тэги'

    def __str__(self):
        return f'{self.tags} {self.recipe}'


class UserRecipeModel(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )

    class Meta:
        abstract = True
        ordering = ('user',)

    def __str__(self):
        return f'{self.user}-{self.recipe}'


class ShoppingCart(UserRecipeModel):
    class Meta(UserRecipeModel.Meta):
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = [UniqueConstraint(fields=['user', 'recipe'],
                                        name='double_shop_cart')]
        default_related_name = 'shopping_cart'


class Favorite(UserRecipeModel):
    class Meta(UserRecipeModel.Meta):
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = [UniqueConstraint(fields=['user', 'recipe'],
                                        name='double_favorited')]
        default_related_name = 'favorite'
