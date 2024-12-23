from django.contrib.auth import get_user_model
from django.urls import reverse
from food.models import Ingredient, IngredientAmount, Recipe, Tag
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class FoodApiTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='db_user')
        self.client.force_authenticate(user=self.user)
        tag = Tag.objects.create(
            name='завтрак',
            color='#0000ff',
            slug='breakfast'
        )
        tag_two = Tag.objects.create(
            name='обед',
            color='#FF0000',
            slug='lunch'
        )
        tag_two.save()

        ingredient = Ingredient.objects.create(
            name='яйцо',
            measurement_unit='шт'
        )
        ingredient_two = Ingredient.objects.create(
            name='молоко',
            measurement_unit='л'
        )
        ingredient_two.save()
        recipe = Recipe.objects.create(
            author=self.user,
            name='Яичница',
            text='Разбей яйца. Пожарь',
            cooking_time='2'
        )
        recipe.tags.add(tag)
        new_recipe = IngredientAmount(
            recipe=recipe,
            ingredient=ingredient,
            amount=10
        )
        new_recipe.save()

    def test_get_recipe_detail(self):
        url_two = reverse('api:recipes-detail', args='1')
        response_two = self.client.get(url_two)
        self.assertEquals(status.HTTP_200_OK, response_two.status_code)

    def test_get_list_recipe(self):
        url = reverse('api:recipes-list')
        response = self.client.get(url)
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(Recipe.objects.count(), 1)

    def test_create(self):
        url = reverse('api:recipes-list')
        image = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAA' \
                'BAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA' \
                '7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5E' \
                'rkJggg=='
        data = {
            'tags': [
                1
            ],
            'ingredients': [
                {
                    'id': 1,
                    'amount': 3
                }
            ],
            'name': 'Яичница-2',
            'image': image,
            'text': 'Разбей яйца и пожарь.',
            'cooking_time': 100
        }
        response = self.client.post(url, data)
        self.assertEquals(status.HTTP_201_CREATED, response.status_code)
        self.assertEquals(Recipe.objects.count(), 2)
        self.assertEquals(Recipe.objects.get(pk=2).name, 'Яичница-2')

    def test_update(self):
        url = reverse('api:recipes-detail', args='1')
        data = {
            'tags': [
                2
            ],
            'ingredients': [
                {
                    'id': 2,
                    'amount': 4
                }
            ],
            'name': 'Омлет',
            'text': 'Разбей яйца, добавь молоко и пожарь.',
            'cooking_time': 10
        }
        response = self.client.patch(url, data)
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(Recipe.objects.get(pk=1).name, 'Омлет')
