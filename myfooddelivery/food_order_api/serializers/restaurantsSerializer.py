from rest_framework import serializers
from ..models import Restaurant
from django.core.validators import  RegexValidator


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'

       

