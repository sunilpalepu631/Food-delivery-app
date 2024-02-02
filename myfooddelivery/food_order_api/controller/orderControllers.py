from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from ..constants.messages import *
from ..models import *
from ..serializers.ordersSerializer import *
from ..helpers.filters import OrderFilter, logFilters
from ..helpers.pagination import *
from ..helpers.sortHelper import sortHelper
from ..middlewares.decoraters import require_token, require_token_admin
from datetime import datetime
from pytz import timezone

class OrdersView():
    @api_view(['POST'])
    @require_token
    def addOrder(request):
        try:
            user_id = request.user.id
            request.data['user'] = user_id
            serializer = PostOrderSerializer(data=request.data)
            
            if serializer.is_valid():
                
                items_data = serializer.validated_data.get('items')
                
                total_price = 0
                
                for item_data in items_data:
                    #just checking the given data is valid or not
                    food_item = FoodItem.objects.get(id=item_data['id'],name = item_data['name'], restaurant=serializer.validated_data.get('restaurant'))
                    quantity = item_data.get('quantity', 1)
                    
                    total_price += food_item.price * quantity
                        

                serializer.validated_data['total_price'] = total_price

                # Save the data to the database
                instance = serializer.save()

                #order log
                Logs.objects.create(
                    order = instance,
                    user = request.user,
                    order_status = 'PAYMENT_PENDING'
                )

                api_url = f'http://{request.get_host()}/orders/start-payment/<int:order_id>/'
                response_data = {
                    **serializer.data,
                    'payment_url': api_url,

                }
                
                return Response({'success': True, 'message': 'Order placed, Payment required', 'data': response_data},status=status.HTTP_402_PAYMENT_REQUIRED)

            return Response({'success': False, 'error': serializer.errors}, status=422)
        except FoodItem.DoesNotExist:
            return Response({'success': False, "error": f"Food item with id {item_data['id']} and '{item_data['name']}' does not exist."}, status=404)
        except Exception as e:
            return Response({'success': False, 'error': str(e)}, status=500)





    @api_view(['PUT'])
    @require_token
    def simulatePaymentView(request, order_id):
        try:
            # Dummy payment simulation
            order = Order.objects.get(id=order_id)
            if order.payment_status == True:
                return Response({'success':False, 'error': 'Already Paid'}, status=400)
            if not request.data.get('payment'):
                return Response({'success': False, 'error': "'payment': [this field is required]"},status=422)

            payment = request.data.get('payment')
            if payment == True:
            
                order.payment_status = True

                local_tz = timezone('Asia/Kolkata')
                order.payment_date = datetime.now(local_tz)

                order.status = 'PAYMENT_DONE'
                order.save()

                #order log
                Logs.objects.create(
                    order = order,
                    user = request.user,
                    order_status = 'PAYMENT_DONE'
                )

                serializer = GetOrderSerializer(order)
                return Response({'success': True, 'message': 'Payment done and order placed successfully', 'data': serializer.data}, status=status.HTTP_200_OK)
            return Response({'success': False, 'error': 'Payment should be true'},status=status.HTTP_402_PAYMENT_REQUIRED)
        except Order.DoesNotExist:
            return Response({'success': False, 'error': 'Order not found'}, status=404)
        except Exception as e:
            return Response({'success': False, 'error': str(e)}, status=500)
        



    @api_view(['POST'])
    @require_token
    @require_token_admin
    def accepted(request, order_id):
        try:
            """Order log to update ACCEPTED"""
            order = Order.objects.get(id=order_id)
            #if order status
            if order.status == 'ACCEPTED':
                return Response({'success': False, 'error': 'Order already accepted'})
            order.status = 'ACCEPTED'
            order.save()
            Logs.objects.create(
                order = order,
                user = request.user,
                order_status = 'ACCEPTED'
            )
            return Response({"success": True, 'message': 'Order accepted Log status updated'}, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({'success': False, 'error': 'Order not found'}, status=404)
        except Exception as e:
            return Response({'success': False, 'error': str(e)}, status=500)
   

    @api_view(['POST'])
    @require_token
    @require_token_admin
    def dispatched(request, order_id):
        ''' ORDER LOG TO UPDATE DISPATCHED AND ASSIGN A RANDOM DELIVERY PERSON'''
        try:
            order = Order.objects.get(id=order_id)

            delivery_persons = DeliveryPerson.objects.all()
            
            if delivery_persons.exists():
                random_delivery_person = random.choice(delivery_persons)
            else:
                random_delivery_person = None

            order.delivery_person = random_delivery_person

            order.status = 'DISPATCHED'
            order.save()


            Logs.objects.create(
                order = order,
                user = request.user,
                order_status = 'DISPATCHED'
            )
            return Response({"success": True, 'message': 'Order dispatched log status updated'}, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({'success': False, 'error': 'Order not found'}, status=404)
        except Exception as e:
            return Response({'success': False, 'error': str(e)}, status=500)
        


    @api_view(['POST'])
    @require_token
    @require_token_admin
    def delivered(request, order_id):
        try:
            order = Order.objects.get(id=order_id)
            order.delivery_status = True
            order.delivered_date = datetime.now()
            order.status = 'DELIVERED'
            order.save()
            # ORDER LOG TO UPDATE DELIVERED
            Logs.objects.create(
                order = order,
                user = request.user,
                order_status = 'DELIVERED'
            )
            return Response({"success": True, 'message': 'Order delivered Log status updated'}, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({'success': False, 'error': 'Order not found'}, status=404)
        except Exception as e:
            return Response({'success': False, 'error': str(e)}, status=500)
        

    



    @api_view(['GET'])
    @require_token
    # @require_token_admin
    def getAllLogs(request):
        try:
            #need to create filters 
            logs = Logs.objects.all()

            filtered_data = logFilters(logs, request)

            serializer = OrderLogSerializer(filtered_data, many=True)

            return Response({"success": True, 'data': serializer.data}, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({'success': False, 'error': 'Order not found'}, status=404)
        except Exception as e:
            return Response({'success': False, 'error': str(e)}, status=500)
        



    @api_view(['GET'])
    @require_token
    @require_token_admin
    def getallOrders(request):
        try:
            Order_data = Order.objects.all()

            #filtering
            filtered_data = OrderFilter(Order_data, request)
            
            #sorting
            sorted_data = sortHelper(filtered_data, request)

            #pagination
            response_data = paginationHelper(sorted_data, request, GetOrderSerializer, SUCCESS_FETCHED_ORDERS)

            return Response(response_data, status=200)
        except Exception as e:
            return Response({'success': False, 'error': str(e)}, status=500)
        
        


    
    @api_view(['GET'])
    @require_token
    def getOneOrder(request,id):
        try:
            user = request.user
            print('user type', type(user))
            queryset = Order.objects.get(id=id, user=user)
            serializer = GetOrderSerializer(queryset)

            return Response({'success': True, 'message': SUCCESS_RETRIEVED_ORDER, 'data': serializer.data},status=200)
        except Order.DoesNotExist:
            return Response({'success': False, 'error': ORDER_NOT_FOUND}, status=404)
        except Exception as e:
            return Response({'success': False, 'error': str(e)}, status=500)
            


    #need to write getallorders of a user when a user is requested
    @api_view(['GET'])
    @require_token
    def getMyOrders(request):
        try:
            user = request.user
            """we can send  'user instance' or 'user ID' to filter"""
            queryset = Order.objects.filter(user=user).order_by('-ordered_date')
            if queryset:
                serializer = GetOrderSerializer(queryset, many=True)
                return Response({'success': True, 'message': SUCCESS_RETRIEVED_MY_ORDERS, 'data': serializer.data},status=200)
            return Response({'success': True, 'message': NO_ORDERS_PLACED},status=200)

        except Order.DoesNotExist:
            return Response({'success': False, 'error': ORDER_NOT_FOUND}, status=404)
        except Exception as e:
            return Response({'success': False, 'error': str(e)}, status=500)







        
    @api_view(['PUT'])
    @require_token
    def updateOrder(request,id):
        try:
            #need to check if order is updating by owner or not
            user_id = request.user.id
            request.data['user'] = user_id

            queryset = Order.objects.get(id=id)

            if queryset.user.id != user_id:
                return Response({'success': False, 'error': 'You do not have permission to update'}, status=403)
            serializer = PostOrderSerializer(queryset, data=request.data)

            if serializer.is_valid():
                items_data = serializer.validated_data.get('items')
                
                total_price = 0

                for item_data in items_data:
                    food_item = FoodItem.objects.get(id=item_data['id'],name = item_data['name'], restaurant=serializer.validated_data.get('restaurant'))
                    quantity = item_data.get('quantity', 1)

                    total_price += food_item.price * quantity
                    
                serializer.validated_data['total_price'] = total_price

                # Save the data to the database
                serializer.save()

            
                return Response({'success': True, 'message': SUCCESS_UPDATED_ORDER, 'data': serializer.data},status=200)
            return Response({'success': False,  'error': serializer.errors}, status=422)
        except Order.DoesNotExist :
            return Response({'success': False, 'error': ORDER_NOT_FOUND}, status=404)
        except FoodItem.DoesNotExist:
            return Response({'success': False, "error": f"Food item with id {item_data['id']} and '{item_data['name']}' does not exist."}, status=404)
        except Exception as e:
            return Response({'success': False, 'error': str(e)}, status=500)
        

        
    #cancel order
    @api_view(['DELETE'])
    @require_token
    def deleteOrder(request,id):
        try:
            user_id = request.user.id
            request.data['user'] = user_id

            order = Order.objects.get(id=id)
            
            if order.user.id != user_id:
                return Response({'success': False, 'error': 'You do not have permission to cancel'}, status=403)

            order.status = 'CANCELLED'
            order.save()

            return Response({'success': True, 'message': "Success cancelled order"},status=200)
        except Order.DoesNotExist:
            return Response({'success': False, 'error': ORDER_NOT_FOUND}, status=404)
        except Exception as e:
            return Response({'success': False, 'error': str(e)}, status=500)
        

