from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.homepage, name='home'),
    path("account/", include('django.contrib.auth.urls')), # contains name='login' url path
    path("signup/", views.SignUp.as_view(), name='signup'),
    path("logout/", views.logout_request, name='logout'),
    path("ingredients/", views.IngredientList.as_view(), name='ingredient_list'),
    path("ingredients/newingredient", views.IngredientCreate.as_view(), name='ingredient_create'),
    path("ingredients/<pk>/updateingredient", views.IngredientUpdate.as_view(), name='ingredient_update'),
    path("ingredients/<pk>/deleteingredient", views.IngredientDelete.as_view(), name='ingredient_delete'),
    path("menulist/", views.MenuList.as_view(), name='menu_list'),
    path("menulist/newmenuitem/", views.MenuCreate.as_view(), name='menu_create'),
    path("menulist/<pk>/updatemenuitem/", views.MenuItemUpdate.as_view(), name='menu_item_update'),
    path("menulist/<pk>/deletemenuitem/", views.MenuDelete.as_view(), name="menu_delete"),
    path("menulist/<menuitem>/recipe/", views.MenuItemRecipeList.as_view(), name='recipe_list'), # Can now use <menuitem> within tmeplate
    path("menulist/<menuitem>/recipe/addingredient", views.RecipeUpdate.as_view(), name='recipe_update'),
    path("menulist/newmenuitem/<menuitem>/newrecipe/", views.RecipeCreate.as_view(), name='recipe_create'),
    path("menulist/<menuitem>/recipe/<pk>/updaterecipeitem/", views.RecipeItemUpdate.as_view(), name='recipe_item_update'),
    path("menutlist/<menuitem>/recipe/<pk>/deleterecipeitem/", views.RecipeItemDelete.as_view(), name='recipe_item_delete'),
    path("purchases/", views.PurchaseList.as_view(), name='purchase_list'),
    path("purchases/create", views.PurchaseCreate.as_view(), name='purchase_create'),
]