from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import UniqueConstraint

from backend.settings import FIELD_TEXT_LENGTH
from users.models import User
from .validators import slug_validator


class Tag(models.Model):
    name = models.CharField(
        'Имя тэга',
        unique=True,
        max_length=FIELD_TEXT_LENGTH
    )
    slug = models.SlugField(
        'Слаг',
        unique=True,
        max_length=200,
        validators=[slug_validator]
    )
    color = models.CharField('Цвет', unique=True, max_length=7)

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self) -> str:
        return self.slug


class Ingredient(models.Model):
    name = models.CharField(
        'Наименование ингредиента',
        max_length=FIELD_TEXT_LENGTH
    )
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=FIELD_TEXT_LENGTH
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self) -> str:
        return self.name + ',' + self.measurement_unit


class Recipe(models.Model):
    tags = models.ManyToManyField(
        Tag,
        through='TagsRecipes',
        verbose_name='Тэги',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name="Автор"
    )
    name = models.CharField(
        max_length=FIELD_TEXT_LENGTH,
        blank=True,
        null=True,
        verbose_name='Название рецепта'
    )
    image = models.ImageField(
        'Фото рецепта',
        upload_to='recipe/images/',
        blank=True
    )
    text = models.CharField(
        max_length=FIELD_TEXT_LENGTH,
        blank=True,
        null=True,
        verbose_name='Описание рецепта'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='ListOfIngredients',
        verbose_name='Ингредиенты',
        blank=True
    )
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления(мин)',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name[:15]

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-id',)


class ListOfIngredients(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Наименование ингредиента',
        related_name='recipe_ingredients'
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='recipe_ingredients',
    )

    class Meta:
        verbose_name = 'Список Ингредиентов'
        verbose_name_plural = 'Списки Ингредиентов'

    def __str__(self) -> str:
        return (
                self.ingredient.name +
                '-' + f'{self.amount}' +
                self.ingredient.measurement_unit
        )


class TagsRecipes(models.Model):
    tags = models.ForeignKey(Tag, on_delete=models.CASCADE)
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
        verbose_name="Рецепт"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь"
    )

    class Meta:
        abstract = True
        ordering = ('user',)

    def __str__(self):
        return f'{self.user}-{self.recipe}'


class ShoppingCart(UserRecipeModel):
    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        default_related_name = 'shopping_cart'


class Favorite(UserRecipeModel):
    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = [UniqueConstraint(fields=['user', 'recipe'],
                                        name='double_favorited')]
        default_related_name = 'favorite'
