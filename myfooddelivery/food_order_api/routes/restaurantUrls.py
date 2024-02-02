from django.contrib import admin
from django.urls import path, include
from  ..controller.restaurantControllers import RestaurantViews


urlpatterns =  [
    path('', RestaurantViews.getAllRestaurants),
    path('add/', RestaurantViews.addRestaurant),

    path('<int:id>', RestaurantViews.getOneRestaurant),
    path('<int:id>/food-items/', RestaurantViews.getOneRestaurantFoodItems),
    path('update/<int:id>', RestaurantViews.updateRestaurant),
    path('delete/<int:id>', RestaurantViews.deleteRestaurant),
]