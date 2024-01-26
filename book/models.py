from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=256, verbose_name='Продукт')
    times_used = models.IntegerField(
        default=0, verbose_name='Раз использовано в рецептах'
    )

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=128, verbose_name='Рецепт')

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class RecipeWithProduct(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name='Продукт'
    )
    weight = models.IntegerField(
        verbose_name='Масса, грамм',
        help_text='Введите массу продукта в граммах'
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Продукты'
        unique_together = ('recipe', 'product')

    def __str__(self):
        return f'№ {self.id}'
