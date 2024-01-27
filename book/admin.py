from django.contrib import admin

from .models import Product, Recipe, RecipeWithProduct


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    ordering = ('id', )
    search_fields = ('name', )
    list_display = ('id', 'name')
    list_display_links = ('name', )


class RecipeWithProductInline(admin.TabularInline):
    model = RecipeWithProduct
    extra = 3


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    ordering = ('id', )
    search_fields = ('name', )
    list_display = ('id', 'name')
    list_display_links = ('name', )
    inlines = (RecipeWithProductInline, )
