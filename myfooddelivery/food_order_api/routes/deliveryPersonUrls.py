from django.contrib import admin
from django.urls import path, include
from  ..controller.deliveryControllers import DeliveryPersonViews

urlpatterns = [
    path('', DeliveryPersonViews.getAllDeliveryPersons),
    path('add/', DeliveryPersonViews.addDeliveryPerson),

    path('<int:id>', DeliveryPersonViews.getOneDeliveryPerson),
    path('update/<int:id>', DeliveryPersonViews.updateDeliveryPerson),
    path('delete/<int:id>', DeliveryPersonViews.deleteDeliveryPerson),

]   