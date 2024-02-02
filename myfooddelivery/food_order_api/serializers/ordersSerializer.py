from rest_framework import serializers

from ..serializers.userSerializer import UserSerializer
from ..models import Logs, Order, User
from ..serializers.foodSerializer import  GetFoodItemSerializer


  
class PostOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        # fields = ['user', 'restaurant', 'total_price', 'items', 'delivery_person']
        fields = '__all__'
       

    def validate_items(self, items_data):
        
        if not items_data:
            raise serializers.ValidationError("At least one food item is required.")

        # Validate each item in the items_data using getFoodItemSerializer
        serializer = GetFoodItemSerializer(data=items_data, many=True)
        if not serializer.is_valid():
            raise serializers.ValidationError(serializer.errors)

        return items_data

    


class GetOrderSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Order
        fields = '__all__'
        depth = 1
       


class OrderLogSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Logs
        fields = '__all__'