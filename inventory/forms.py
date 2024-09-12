from django import forms
from .models import Ingredient, MenuItem, RecipeRequirement, Purchase

class MenuForm(forms.ModelForm):
    """Form for menu items"""
    class Meta:
        model = MenuItem
        fields = '__all__'

class RecipeForm(forms.ModelForm):
    """Form for recipes"""
    class Meta:
        model = RecipeRequirement
        fields = '__all__'

class IngredientForm(forms.ModelForm):
    """Form for ingredients"""
    class Meta:
        model = Ingredient
        fields = ["name", "unit_price", "total_quantity", "unit_of_measure"]

class PurchaseForm(forms.ModelForm):
    """Form for purchases"""
    class Meta:
        model = Purchase
        fields = '__all__'

