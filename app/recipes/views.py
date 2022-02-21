from rest_framework import viewsets, mixins

from recipes.models import Recipe, Ingredient

from recipes import serializers


class RecipesViewSet(viewsets.ModelViewSet):
    """Manage recipes in the database"""
    serializer_class = serializers.RecipeSerializer
    queryset = Recipe.objects.all()

    def get_queryset(self):
        """Retrieve the recipes"""
        name = self.request.query_params.get('name')
        if name:
            self.queryset = self.queryset.filter(name__icontains=name)
        return self.queryset
