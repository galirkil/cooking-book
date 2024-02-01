from django.db import IntegrityError
from django.db.models import F
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_list_or_404, get_object_or_404, render

from .models import Product, Recipe, RecipeWithProduct


def add_product_to_recipe(request: HttpRequest, recipe_id: int,
                          product_id: int, weight: int) -> HttpResponse:
    """
    Adds a product and its weight to the specified recipe.
    If the recipe already contains such a product, its weight
    will be changed to the specified one.
    """
    try:
        RecipeWithProduct.objects.update_or_create(
            recipe_id=recipe_id, product_id=product_id,
            defaults={'weight': weight}
        )
    except IntegrityError:
        try:
            Recipe.objects.get(id=recipe_id)
        except Recipe.DoesNotExist:
            return HttpResponse(
                'Указанный рецепт отсутствует в базе данных!', status=404
            )
        try:
            Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return HttpResponse(
                'Указанный продукт отсутствует в базе данных!', status=404
            )
    else:
        return HttpResponse("Продукт добавлен в рецепт!", status=200)


def cook_recipe(request: HttpRequest, recipe_id: int) -> HttpResponse:
    """
    Increases 'times used' attribute for each product in requested recipe
    """
    products_in_recipe = Product.objects.filter(
        recipewithproduct__recipe_id=recipe_id
    ).update(times_used=F('times_used') + 1)
    if products_in_recipe:
        return HttpResponse('Блюдо приготовлено!', status=200)
    return HttpResponse('Блюдо не найдено!', status=404)


def show_recipes_without_product(request: HttpRequest,
                                 product_id: int) -> HttpResponse:
    """
    Renders page with list of recipes without requested product in them
    and recipes which contain less than 10 grams of requested product
    """
    product = get_object_or_404(Product, id=product_id)
    recipes_without_product = Recipe.objects.exclude(
        recipewithproduct__product__id=product_id
    )
    recipes_with_product_less_than_10_grams = Recipe.objects.filter(
        recipewithproduct__product__id=product_id,
        recipewithproduct__weight__lt=10
    )
    recipes = recipes_without_product.union(
        recipes_with_product_less_than_10_grams
    )

    return render(request, 'recipes.html',
                  {'recipes': recipes, 'product_name': product.name})
