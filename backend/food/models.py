from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from django.db.models import UniqueConstraint

User = get_user_model()


class Tag(models.Model):
    """Модель для тегов."""
    name = models.CharField(
        unique=True,
        max_length=20,
        verbose_name='Название тега'
    )
    color = models.CharField(
        unique=True,
        max_length=7,
        verbose_name='Цвет',
        validators=[
            RegexValidator(
                regex='^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$',
                message='Вы ввели цвет не в формате HEX'
            )
        ]
    )
    slug = models.SlugField(
        unique=True,
        db_index=True,
        verbose_name='Идентификатор')

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Модель для ингредиентов."""
    name = models.CharField(
        max_length=200,
        verbose_name='Название ингредиента')
    measurement_unit = models.CharField(
        max_length=20,
        verbose_name='Единица измерения')

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель для рецептов."""
    author = models.ForeignKey(
        User,
        related_name='recipes',
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Автор рецепта'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientAmount',
        related_name='recipes',
        verbose_name='Ингредиент',
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Тег'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )
    image = models.ImageField(
        verbose_name='Изображение рецепта',
        upload_to='food/',
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название')
    text = models.CharField(
        max_length=2000,
        verbose_name='Описание')
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время готовки',
        validators=[MinValueValidator(
            1, message='Укажите время готовки'
        )]
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.name


class IngredientAmount(models.Model):
    """Модель, отвечающая за количество ингредиентов в рецепте.
    Связывает модели Recipe и Ingredient."""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredient_list',
        verbose_name='Рецепт'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipe',
        verbose_name='Ингредиент'
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        validators=[MinValueValidator(
            1, message='Укажите количество ингредиентов')]
    )

    class Meta:
        verbose_name = 'Ингредиент в рецепте',
        verbose_name_plural = 'Ингредиентов в рецепте'

    def __str__(self):
        return f''' {self.recipe.name} - {self.ingredient.name} -
        {self.amount} {self.ingredient.measurement_unit}'''


class Favourite(models.Model):
    """Модель избранного."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = [
            UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favourite'
            )
        ]

    def __str__(self):
        return f'{self.recipe} добавлен {self.user} в избранное'


class ShoppingCart(models.Model):
    """Модель списка покупок."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = [
            UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_shopping_cart'
            )
        ]

    def __str__(self):
        return f'{self.recipe} добавлен {self.user} в список покупок'
