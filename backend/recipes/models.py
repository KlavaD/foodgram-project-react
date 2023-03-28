from django.core.validators import MinValueValidator
from django.db import models

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
        return self.name


class ListOfIngredients(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        'Наименование ингредиента',
        db_index=True,
        max_length=FIELD_TEXT_LENGTH
    )
    amount = models.IntegerField(
        validators=[
            MinValueValidator(1, "Значение не меньше %(limit_value).")],
        verbose_name='Количество'
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


class Recipe(models.Model):
    tags = models.ManyToManyField(
        Tag,
        through='TagsRecipes',
        verbose_name='Тэги',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор"
    )
    ingredients = models.ManyToManyField(
        ListOfIngredients,
        related_name='recipe',
        verbose_name='Ингредиенты',
    )
    is_favorited = models.BooleanField(
        default=False,
        verbose_name='В избранном'
    )
    is_in_shopping_cart = models.BooleanField(
        default=False,
        verbose_name='В корзине'
    )
    name = models.TextField(
        max_length=FIELD_TEXT_LENGTH,
        verbose_name='Название рецепта'
    )
    image = models.ImageField(
        'Фото рецепта',
        upload_to='recipe/images/',
        blank=True
    )
    text = models.TextField(
        verbose_name='Описание рецепта'
    )
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления',
    )

    def __str__(self):
        return self.name[:15]

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-id',)


class TagsRecipes(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Рецепт:Тэги'
        verbose_name_plural = 'Рецепты:Тэги'

    def __str__(self):
        return f'{self.tag} {self.recipe}'


class UserRecipeModel(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE
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


class Favorite(UserRecipeModel):
    class Meta:
        verbose_name = 'Избранное'
