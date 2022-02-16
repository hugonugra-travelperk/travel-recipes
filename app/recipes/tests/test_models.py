from django.test import TestCase
from recipes import models


# Create your tests here.
class ModelTests(TestCase):
    def test_recipe_str(self):
        """Test the recipe string representation"""
        recipe = models.Recipe.objects.create(
            name='Ayampaco',
            description='chicken envolved by leafs',
        )

        self.assertEqual(str(recipe), recipe.name)

    def test_ingredient_str(self):
        """Test the recipe string representation"""
        recipe = models.Recipe.objects.create(
            name='Ayampaco',
            description='chicken envolved by leafs',
        )

        ingredient = models.Ingredient.objects.create(
            name='Chicken',
            recipe=recipe,
        )

        self.assertEqual(str(ingredient), ingredient.name)
