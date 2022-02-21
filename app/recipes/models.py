from django.db import models


# Create your models here.

class Recipe(models.Model):
    """Recipe object"""
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=2047)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Recipe object"""
    name = models.CharField(max_length=255)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ingredients')

    def __str__(self):
        return self.name
