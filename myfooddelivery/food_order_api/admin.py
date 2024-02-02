from django.contrib import admin
from .models import Restaurant, User, FoodItem, DeliveryPerson, Order, Logs

admin.site.register(Restaurant)
admin.site.register(User)
admin.site.register(FoodItem)
admin.site.register(DeliveryPerson)
admin.site.register(Order)
admin.site.register(Logs)


