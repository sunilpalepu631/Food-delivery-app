from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from ..constants.messages import *
from ..models import *
from ..serializers.deliverySerializer import *
from ..helpers.filters import DeliveryPersonFilter
from ..helpers.pagination import paginationHelper
from ..helpers.sortHelper import sortHelper
from ..middlewares.decoraters import require_token, require_token_admin



class DeliveryPersonViews():
    @api_view(['POST'])
    @require_token
    @require_token_admin
    def addDeliveryPerson(request):
        try:
            serializer = DeliveryPersonSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()

                return Response({'success': True, 'message': SUCCESS_REGISTERED_DELIVERY_PERSON, 'data': serializer.data},status=201)
            return Response({'success': False, 'error': serializer.errors}, status=422)
        except Exception as e:
            return Response({'success': False, 'error': str(e)}, status=500)



    @api_view(['GET'])
    @require_token
    @require_token_admin
    def getAllDeliveryPersons(request):
        try:
            delivery_person_data = DeliveryPerson.objects.all()

            #filtering
            filtered_data = DeliveryPersonFilter(delivery_person_data, request)
            
            #sorting
            sorted_data = sortHelper(filtered_data, request)

            #pagination
            response_data = paginationHelper(sorted_data, request, DeliveryPersonSerializer, SUCCESS_FETCHED_DELIVERY_PERSONS)
            
            return Response(response_data, status=200)
        except Exception as e:
            return Response({'success': False, 'error': str(e)}, status=500)


    

    
    @api_view(['GET'])
    @require_token
    @require_token_admin
    def getOneDeliveryPerson(request,id):
        try:
            queryset = DeliveryPerson.objects.get(id=id)
            serializer = DeliveryPersonSerializer(queryset)

            return Response({'success': True, 'message': SUCCESS_RETRIEVED_DELIVERY_PERSON, 'data': serializer.data},status=200)
        except DeliveryPerson.DoesNotExist:
            return Response({'success': False, 'error': DELIVERYPERSON_NOT_FOUND}, status=404)
        except Exception as e:
            return Response({'success': False, 'error': str(e)}, status=500)
            
        

        
    @api_view(['PUT'])
    @require_token
    @require_token_admin
    def updateDeliveryPerson(request,id):
        try:
            queryset = DeliveryPerson.objects.get(id=id)
            serializer = DeliveryPersonSerializer(queryset, data=request.data)
            if serializer.is_valid():
                serializer.save()

                return Response({'success': True, 'message': SUCCESS_UPDATED_DELIVERY_PERSON, 'data': serializer.data},status=200)
            return Response({'success': False, 'error': serializer.errors}, status=422)
        except DeliveryPerson.DoesNotExist:
            return Response({'success': False, 'message': DELIVERYPERSON_NOT_FOUND}, status=404)
        except Exception as e:
            return Response({'success': False, 'error': str(e)}, status=500)
        

        
          
    @api_view(['DELETE'])
    @require_token
    @require_token_admin
    def deleteDeliveryPerson(request,id):
        try:
            queryset = DeliveryPerson.objects.get(id=id)
            queryset.delete()

            return Response({'success': True, 'message': SUCCESS_DELETED_DELIVERY_PERSON},status=200)
        except DeliveryPerson.DoesNotExist:
            return Response({'success': False, 'error': DELIVERYPERSON_NOT_FOUND}, status=404)
        except Exception as e:
            return Response({'success': False, 'error': str(e)}, status=500)
        


