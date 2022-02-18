from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from recipes.models import Recipe, Ingredient

from recipes.serializers import RecipeSerializer, IngredientSerializer

RECIPES_URL = reverse('recipes:recipe-list')


def detail_url(recipe_id):
    """Return recipe detail URL"""
    return reverse('recipes:recipe-detail', args=[recipe_id])


def sample_ingredient(recipe, name='Chicken'):
    """Create and return a sample ingredient"""
    return Ingredient.objects.create(recipe=recipe, name=name)


def sample_recipe(**params):
    """Create and return a sample recipe"""
    default_params = {
        'name': 'Ayampaco',
        'description': 'Chicken surrounded by leafs',
    }
    default_params.update(params)

    return Recipe.objects.create(**default_params)


class PublicRecipeApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_retrieve_recipes_without_filters(self):
        """Test retrieving a list of recipes without filtering"""
        sample_recipe()
        sample_recipe()

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.all()
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_recipes_with_filters(self):
        """Test retrieving a list of recipes without filtering"""
        searching_param = 'bol'

        sample_recipe(name='humita')
        sample_recipe(name='bolon')

        res = self.client.get(RECIPES_URL + '?name=' + searching_param)

        recipes = Recipe.objects.filter(name__contains=searching_param)
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_view_recipe_detail(self):
        """Test viewing a recipe detail"""
        recipe = sample_recipe()
        sample_ingredient(recipe)

        url = detail_url(recipe.id)
        res = self.client.get(url)

        serializer = RecipeSerializer(recipe)
        self.assertEqual(res.data, serializer.data)

    def test_create_recipe(self):
        """Test creating a recipe"""
        payload = {
            'name': 'Quimbolito',
            'description': 'Corn mass cooked with leafs',
            'ingredients': [{'name': 'Corn'}, {'name': 'Achira leafs'}],
        }
        res = self.client.post(RECIPES_URL, payload, 'json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])

        self.assertEqual(payload['name'], recipe.name)
        self.assertEqual(payload['description'], recipe.description)
        self.assertEqual(recipe.ingredients.count(), 2)
        self.assertEqual(recipe.ingredients.filter(name='Corn').count(), 1)
        self.assertEqual(recipe.ingredients.filter(name='Achira leafs').count(), 1)

    def test_update_recipe_without_ingredients(self):
        """Test updating a recipe with patch"""
        recipe = sample_recipe()
        sample_ingredient(recipe)

        payload = {'name': 'New ayampaco', 'description': 'a new description'}
        url = detail_url(recipe.id)
        self.client.patch(url, payload, 'json')

        recipe.refresh_from_db()
        self.assertEqual(recipe.name, payload['name'])
        self.assertEqual(recipe.description, payload['description'])
        self.assertEqual(recipe.ingredients.count(), 1)

    def test_update_recipe_with_ingredients(self):
        """Test updating a recipe with patch"""
        recipe = sample_recipe()
        ingredient = sample_ingredient(recipe)

        payload = {
            'name': 'New ayampaco',
            'description': 'a new description',
            'ingredients': [{'name': 'other ingredient 1'}, {'name': 'other ingredient 2'}]
        }
        url = detail_url(recipe.id)
        self.client.patch(url, payload, 'json')

        deleting_ingredient_serializer = IngredientSerializer(ingredient)
        ingredients = Ingredient.objects.all()
        all_ingredients_serializer = IngredientSerializer(ingredients, many=True)

        recipe.refresh_from_db()
        self.assertEqual(recipe.name, payload['name'])
        self.assertEqual(recipe.description, payload['description'])
        self.assertEqual(recipe.ingredients.count(), 2)
        self.assertNotIn(deleting_ingredient_serializer.data, all_ingredients_serializer.data)
        self.assertEqual(recipe.ingredients.filter(name='other ingredient 1').count(), 1)
        self.assertEqual(recipe.ingredients.filter(name='other ingredient 2').count(), 1)

    def test_delete_recipe(self):
        """Test deleting a recipe with delete"""
        recipe = sample_recipe()
        sample_ingredient(recipe)
        sample_ingredient(recipe)

        url = detail_url(recipe.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Recipe.objects.all().count(), 0)
        self.assertEqual(Ingredient.objects.all().count(), 0)
