from ..constants.messages import *
from ..models import *
from ..serializers.restaurantsSerializer import *
from ..serializers.foodSerializer import *
from ..helpers.filters import RestaurantFilter
from ..helpers.pagination import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from ..helpers.sortHelper import sortHelper
from ..middlewares.decoraters import *




class RestaurantViews():
    #todo
    #need to add pagination
    @api_view(['GET'])
    @require_token
    def getAllRestaurants(request):
        try:
            restaurant_data = Restaurant.objects.all()

            #filtering
            filtered_data = RestaurantFilter(restaurant_data, request)
            
            #sorting
            sorted_data = sortHelper(filtered_data, request)

            #pagination
            response_data = paginationHelper(sorted_data, request, RestaurantSerializer, SUCCESS_FETCHED_RESTAURANTS)
            
            return Response(response_data, status=200)
        except Exception as e:
            return Response({'success': False,  'error': str(e)}, status=500)
            


    @api_view(['POST'])
    @require_token
    @require_token_admin
    def addRestaurant(request):
        try:
            serializer = RestaurantSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()

                return Response({'success': True, 'message': SUCCESS_REGISTERED_RESTAURANT, 'data': serializer.data},status=201)
            return Response({'success': False, 'error': serializer.errors}, status=422)
        except Exception as e:
            return Response({'success': False, 'error': str(e)}, status=500)


    @api_view(['GET'])
    @require_token
    def getOneRestaurant(request,id):
        try:
            queryset = Restaurant.objects.get(id=id)
            serializer = RestaurantSerializer(queryset)

            return Response({'success': True, 'message': SUCCESS_RETRIEVED_RESTAURANT, 'data': serializer.data},status=200)
        except Restaurant.DoesNotExist:
            return Response({'success': False, 'error': RESTAURANT_NOT_FOUND,}, status=404)
        except Exception as e:
            return Response({'success': False, 'error': str(e)}, status=500)
        




    @api_view(['GET'])
    @require_token
    def getOneRestaurantFoodItems(request,id):
        try:
            #need to handle exception properly
            Restaurant.objects.get(id=id)
            food_items_queryset = FoodItem.objects.filter(restaurant=id)

            if food_items_queryset:

                restaurnat_name = food_items_queryset[0].restaurant.name
                print(restaurnat_name)
                response_data = []

                serializer = GetFoodItemSerializer(food_items_queryset, many=True)
                modify_data = {
                    'restaurant_id': id,
                    'restaurant_name': restaurnat_name,
                    'menu': serializer.data
                }

                response_data.append(modify_data)

                return Response({'success': True, 'message': SUCCESS_RETRIEVED_FOOD_ITEMS_IN_RESTAURANT, 'data': response_data},status=200)
            return Response({'success': True, 'message': 'Food itmes not added', 'data': []},status=200)
        except Restaurant.DoesNotExist:
            return Response({'success': False, 'error': RESTAURANT_NOT_FOUND}, status=404)
        except Exception as e:
            return Response({'success': False, 'error': str(e)}, status=500)
            
        


    @api_view(['PUT'])
    @require_token
    @require_token_admin
    def updateRestaurant(request,id):
        try:
            queryset = Restaurant.objects.get(id=id)
            serializer = RestaurantSerializer(queryset, data=request.data)
            if serializer.is_valid():
                serializer.save()

                return Response({'success': True, 'message': SUCCESS_UPDATED_RESTAURANT, 'data': serializer.data},status=200)
            return Response({'success': False,  'error': serializer.errors}, status=422)
        except Restaurant.DoesNotExist as e:
            return Response({'success': False, 'error':RESTAURANT_NOT_FOUND}, status=404)
        except Exception as e:
            return Response({'success': False, 'error': str(e)}, status=500)
        

        
        
    @api_view(['DELETE'])
    @require_token
    @require_token_admin
    def deleteRestaurant(request,id):
        try:
            queryset = Restaurant.objects.get(id=id)
            queryset.delete()

            return Response({'success': True, 'message': SUCCESS_DELETED_RESTAURANT},status=200)
        except Restaurant.DoesNotExist:
            return Response({'success': False, 'error': RESTAURANT_NOT_FOUND}, status=404)
        except Exception as e:
            return Response({'success': False, 'error': str(e)}, status=500)
        