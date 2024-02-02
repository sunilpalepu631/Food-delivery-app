from django.contrib import admin
from django.urls import path, include
from ..controller.foodItemsControllers import FoodItemsViews

urlpatterns = [
    path('', FoodItemsViews.getAllFoodItems),
    path('add/', FoodItemsViews.addFoodItem),
    
    path('<int:id>', FoodItemsViews.getOneFoodItem),
    path('update/<int:id>', FoodItemsViews.updateFoodItem),
    path('delete/<int:id>', FoodItemsViews.deleteFoodItem),
]