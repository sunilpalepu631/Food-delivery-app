from rest_framework import serializers
from ..models import FoodItem
from rest_framework.validators import ValidationError


class FoodItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodItem
        fields = '__all__'
        depth = 1



class PostFoodItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodItem
        fields = '__all__'
        
   

class GetFoodItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodItem
        fields = ['id', 'name', 'food_type', 'price']


    
class PostOrderFoodItemSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=20)
    quantity = serializers.IntegerField(required=False, default=1)
