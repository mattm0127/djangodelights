from django.db.models import Sum
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Ingredient, MenuItem, RecipeRequirement, Purchase
from .forms import MenuForm, RecipeForm, IngredientForm, PurchaseForm
from decimal import Decimal
# Create your views here.

def homepage(request):
    return render(request, 'inventory/home.html')

class SignUp(CreateView):
    form_class = UserCreationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy('login') # Goes from /login in reverse so : /accounts/login

class IngredientCreate(LoginRequiredMixin, CreateView):
    model = Ingredient
    form_class = IngredientForm
    template_name = "inventory/ingredient_create.html"
    success_url = "/ingredients/"

class IngredientList(LoginRequiredMixin, ListView):
    model = Ingredient
    template_name = 'inventory/ingredient_list.html'
    
    def get_context_data(self):
        total_value = Ingredient.objects.aggregate(total=Sum('value'))
        context= super().get_context_data()
        try:
            context['total_value'] = round(total_value['total'], 2)
        except:
            context['total_value'] = '0.00'
        return context

class IngredientUpdate(LoginRequiredMixin, UpdateView):
    model = Ingredient
    form_class = IngredientForm
    template_name = 'inventory/ingredient_update_form.html'
    success_url = '/ingredients'

class IngredientDelete(LoginRequiredMixin, DeleteView):
    model = Ingredient
    template_name = 'inventory/ingredient_delete_form.html'
    success_url = '/ingredients/'

class MenuCreate(LoginRequiredMixin, CreateView):
    model = MenuItem
    form_class = MenuForm
    template_name = "inventory/menu_create_form.html"

    def get_success_url(self):
        menuitem = MenuItem.objects.last().name # Returns the last object created name
        return reverse_lazy('recipe_create', kwargs={'menuitem': menuitem})

class MenuList(LoginRequiredMixin, ListView):
    model = MenuItem
    template_name = "inventory/menu_item_list.html"

class MenuDelete(LoginRequiredMixin, DeleteView):
    model = MenuItem
    template_name = 'inventory/menu_delete_form.html'
    success_url = '/menulist'

class MenuItemRecipeList(LoginRequiredMixin, ListView):
    template_name = 'inventory/recipe_by_menuitem.html'
    model = RecipeRequirement
    
    def get_queryset(self):
        """Returns the queryset of only the menu_itm that was clicked."""
        self.menuitem = get_object_or_404(MenuItem, name=self.kwargs['menuitem']) # kwargs pulls the url tag
        return RecipeRequirement.objects.filter(menu_item=self.menuitem)
    
    def get_context_data(self, **kwargs):
        # Call the current database
        context = super().get_context_data(**kwargs)
        # Add the key: value
        context['menuitem'] = self.menuitem
        return context

class MenuItemUpdate(LoginRequiredMixin, UpdateView): # Update view looks for <pk> from url
    model = MenuItem
    form_class = MenuForm
    template_name = 'inventory/menu_item_update_form.html'
    success_url = '/menulist/'

class RecipeCreate(LoginRequiredMixin,CreateView):
    model = RecipeRequirement
    form_class = RecipeForm
    template_name = "inventory/recipe_create_form.html"
    
    def get_success_url(self):
        menuitem = get_object_or_404(MenuItem, name=self.kwargs['menuitem'])
        return reverse_lazy('recipe_create', kwargs={'menuitem': menuitem})
    
    def get_form(self, *args, **kwargs): # will only allow specified queryset as drop down for menu_item form field
        menuitem = get_object_or_404(MenuItem, name=self.kwargs['menuitem'])
        form = super(RecipeCreate, self).get_form(*args, **kwargs)
        form.fields['menu_item'].queryset = MenuItem.objects.filter(name=menuitem)
        return form

class RecipeUpdate(LoginRequiredMixin, CreateView):
    model = RecipeRequirement
    form_class = RecipeForm
    template_name = 'inventory/recipe_create_form.html'

    def get_success_url(self):
        menuitem = get_object_or_404(MenuItem, name=self.kwargs['menuitem'])
        return reverse_lazy('recipe_create', kwargs={'menuitem': menuitem})

    def get_context_data(self):
        menu_item = get_object_or_404(MenuItem, name= self.kwargs['menuitem'])
        context = super().get_context_data()
        context['menuitem'] = menu_item
        return context
    
    def get_form(self, *args, **kwargs): # will only allow specified queryset as drop down for menu_item form field
        menuitem = get_object_or_404(MenuItem, name=self.kwargs['menuitem'])
        form = super(RecipeUpdate, self).get_form(*args, **kwargs)
        form.fields['menu_item'].queryset = MenuItem.objects.filter(name=menuitem)
        return form   
    
class RecipeItemUpdate(LoginRequiredMixin, UpdateView):
    model = RecipeRequirement
    template_name = 'inventory/recipe_item_update_form.html' 
    fields = ["ingredient", "amount_used"]
    
    def get_success_url(self): # THIS IS IT! Add kwarg to URL to return to a name specific page
        return reverse_lazy('recipe_list', kwargs={'menuitem': self.object.menu_item})

class RecipeItemDelete(LoginRequiredMixin, DeleteView):
    model = RecipeRequirement
    template_name = "inventory/recipe_item_delete_form.html"
    
    def get_success_url(self):
        return reverse_lazy('recipe_list', kwargs={'menuitem': self.object.menu_item})

class PurchaseCreate(LoginRequiredMixin, CreateView):
    model = Purchase
    fields = ['menu_item']
    template_name = "inventory/purchase_create_form.html"
    success_url = '/purchases/'

class PurchaseList(LoginRequiredMixin, ListView):
    model = Purchase
    template_name = 'inventory/purchase_list.html'

    def get_context_data(self):
        total_profit = Purchase.objects.aggregate(profit=Sum('profit')) # aggregate returns dict_key=Sum('Key in Model')
        total_cost = Purchase.objects.aggregate(cost=Sum('cost'))
        total_revenue = Purchase.objects.aggregate(price=Sum('price'))
        context = super().get_context_data()
        try:
            context['total_profit'] = round(total_profit['profit'], 2) #Retrieve the total profit value from profit key in total_profit dict
            context['total_cost'] = round(total_cost['cost'],2)
            context['total_revenue'] = round(total_revenue['price'],2)
        except:
            context['total_profit'] = '0.00' # Return 0.00 if no values for round() ---> crashes otherwise
            context['total_cost'] = '0.00'
            context['total_revenue'] = '0.00'
        return context

def logout_request(request): 
    logout(request)
    return redirect('home')