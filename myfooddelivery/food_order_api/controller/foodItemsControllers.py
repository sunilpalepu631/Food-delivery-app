from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from ..constants.messages import *
from ..models import *
from ..serializers.foodSerializer import PostFoodItemSerializer, FoodItemSerializer
from ..helpers.filters import FoodItemFilter
from ..helpers.pagination import paginationHelper
from ..helpers.sortHelper import sortHelper
from ..middlewares.decoraters import require_token_admin, require_token




class FoodItemsViews():
    @api_view(['POST'])
    @require_token
    @require_token_admin
    def addFoodItem(request):
        try:
            serializer = PostFoodItemSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()

                return Response({'success': True, 'message': SUCCESS_ADD_FOODITEM, 'data': serializer.data},status=201)
            return Response({'success': False, 'errors': serializer.errors}, status=422)
            
        except Exception as e:
            return Response({'success': False, 'message':UNEXPECTED_ERROR, 'error': str(e)}, status=500)          


    @api_view(['GET'])
    @require_token
    def getAllFoodItems(request):
        try:
            food_items_data = FoodItem.objects.all()

            #filtering
            filtered_data = FoodItemFilter(food_items_data, request)
            
            #sorting
            sorted_data = sortHelper(filtered_data, request)

            #pagination
            response_data = paginationHelper(sorted_data, request, FoodItemSerializer, SUCCESS_FETCHED_DELIVERY_PERSONS)
            
            return Response(response_data, status=200)
        except Exception as e:
            return Response({'success': False, 'error': str(e)}, status=500)   



    @api_view(['GET'])
    @require_token
    def getOneFoodItem(request,id):
            try:
                queryset = FoodItem.objects.get(id=id)
                serializer = FoodItemSerializer(queryset)

                return Response({'success': True, 'message': SUCCESS_FETCHED_FOODITEM, 'data': serializer.data},status=200)
            except FoodItem.DoesNotExist as e:
                return Response({'success': False, 'error': FOOD_ITEM_NOT_FOUND}, status=404)
            except Exception as e:
                return Response({'success': False, 'error': str(e)}, status=500) 
            
        


    @api_view(['PUT'])
    @require_token
    @require_token_admin
    def updateFoodItem(request,id):
        try:
            queryset = FoodItem.objects.get(id=id)
            serializer = FoodItemSerializer(queryset, data=request.data)
            if serializer.is_valid():
                serializer.save()

                return Response({'success': True, 'message': SUCCESS_UPDATED_FOODITEM, 'data': serializer.data},status=200)
            return Response({'success': False,  'error': serializer.errors}, status=422)
        except Restaurant.DoesNotExist as e:
            return Response({'success': False, 'error':FOOD_ITEM_NOT_FOUND, 'error': str(e)}, status=404)
        except Exception as e:
            return Response({'success': False, 'error': str(e)}, status=500)
        

        
    @api_view(['DELETE'])
    @require_token
    @require_token_admin
    def deleteFoodItem(request,id):
        try:
            queryset = FoodItem.objects.get(id=id)
            queryset.delete()

            return Response({'success': True, 'message': SUCCESS_DELETED_FOODITEM},status=200)
        except FoodItem.DoesNotExist as e:
            return Response({'success': False, 'error': FOOD_ITEM_NOT_FOUND}, status=404)
        except Exception as e:
            return Response({'success': False,  'error': str(e)}, status=500)
        

