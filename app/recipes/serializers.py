from rest_framework import serializers

from recipes.models import Recipe, Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    """Serialize for ingredient objects"""

    class Meta:
        model = Ingredient
        fields = ('id', 'name')
        read_only_fields = ('id',)


class RecipeSerializer(serializers.ModelSerializer):
    """Serialize for recipe objects"""
    ingredients = IngredientSerializer(
        many=True,
    )

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'description', 'ingredients')
        read_only_fields = ('id',)

    def create(self, validated_data):
        new_ingredients = validated_data.pop('ingredients')
        new_recipe = Recipe.objects.create(**validated_data)

        for new_ingredient in new_ingredients:
            Ingredient.objects.create(recipe=new_recipe, name=new_ingredient['name'])

        return new_recipe

    def update(self, instance, validated_data):
        new_ingredients = validated_data.pop('ingredients', [])
        if len(new_ingredients) > 0:
            instance.ingredients.all().delete()
            for new_ingredient in new_ingredients:
                Ingredient.objects.create(recipe=instance, name=new_ingredient['name'])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance
