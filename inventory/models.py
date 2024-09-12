from django.db import models
from django.urls import reverse_lazy
from decimal import Decimal
from django.db.models import Sum

# Create your models here.
class Ingredient(models.Model):
    """Model for individual ingredients."""
    name = models.CharField(max_length=50)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit_of_measure = models.CharField(max_length=10, blank=True)
    value = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.value = self.get_value()
        super(Ingredient, self).save(*args, **kwargs)
    
    def get_value(self):
        value = (self.unit_price * self.total_quantity)
        return value

class MenuItem(models.Model):
    """Model for individual Menu Items."""
    name = models.CharField(max_length=70)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class RecipeRequirement(models.Model):
    """Model for recipe per ingredient"""
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount_used = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.menu_item}: {self.ingredient}"   

class Purchase(models.Model):
    """Model for each purchase made"""
    date = models.DateTimeField(auto_now=True)
    menu_item = models.ForeignKey(MenuItem, null=True, on_delete=models.SET_NULL)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    profit = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    def __str__(self):
        return f"{self.date}: {self.menu_item}"

    def save(self, *args, **kwargs):
        self.price = self.menu_item.price
        self.cost = self.get_cost()
        self.profit = self.price - self.cost
        for item in self.recipe:
            item.ingredient.total_quantity -= item.amount_used
            item.ingredient.value = item.ingredient.get_value()
            super(Ingredient, item.ingredient).save(*args, **kwargs)
        super(Purchase, self).save(*args, **kwargs)
    
    def get_cost(self):
        self.recipe = self.menu_item.reciperequirement_set.all()
        item_prices = []
        for item in self.recipe:
            item_cost = item.ingredient.unit_price * item.amount_used
            item_prices.append(item_cost)
        return sum(item_prices)
    
    