from ..helpers.filters import userFilters
from ..helpers.pagination import paginationHelper
from ..helpers.sortHelper import sortHelper
from ..models import *
from ..constants.messages import *
from ..serializers.userSerializer import *
from ..middlewares.decoraters import *
from django.contrib.auth.hashers import check_password
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status




class UserViews():
    #create
    
    @api_view(['POST'])
    def registerUser(request):
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                
                # refresh = RefreshToken.for_user(user)

                # refresh_token = str(refresh)
                # access_token = str(refresh.access_token)

                # serializer.data['access_token'] = access_token
                # serializer.data['refresh_token'] = refresh_token


                # response_data = {
                # 'success': True,
                # 'message': SUCCESS_REGISTERED_USER,
                # 'data': {
                #     **serializer.data,  # Include existing serializer data
                #     'access_token': access_token,
                #     'refresh_token': refresh_token,
                #     }
                # }
                
                return Response({'success': True, 'message': 'User successfully registered', 'data': serializer.data},status=201)
            return Response({'success': False, 'error': serializer.errors}, status=422)
        
        except Exception as e:
            return Response({'success': False, 'error': str(e)}, status=500)
        
    

    @api_view(['POST'])
    def loginUser(request):
        try:
            serializer = UserLoginSerializer(data=request.data)

            if serializer.is_valid():

                username = serializer.validated_data.get('username')
                password = serializer.validated_data.get('password')

                #fetching user detalis using username
                user = User.objects.get(username=username)

                #if user found: checking password
                if check_password(password=password, encoded=user.password):
                    refresh = RefreshToken.for_user(user)

                    refresh_token = str(refresh)
                    access_token = str(refresh.access_token)
                    
                    return Response({'success':True, 'message': SUCCESS_PASSWORD_CORRECT, 'access_token': access_token, 'refresh_token': refresh_token},status=200)
                return Response({'success': False,'error': INVALID_PASSWORD}, status=401) 
            return Response({'success': False, 'error': serializer.errors}, status=422)
        except User.DoesNotExist:
            return Response({'success': False, 'error': INVALID_USERNAME},status=401)
        except Exception as e:
            return Response({'success': False, 'error': str(e)},status=500)  

# raise exceptions.AuthenticationFailed(
#             'username and password required')

    @api_view(['POST'])
    def getAccessToken(request):
        """generates a new access token from the refresh token."""
        try:
            refresh_token = request.data.get('refresh_token')
            if not refresh_token:
                return Response({'success': False, 'error': "'refresh_token' field must be included"},status=422)
            
            new_token = RefreshToken(refresh_token)
            access_token = str(new_token.access_token)

            return Response({'success':True, 'message':'Access token generated successfully', 'access_token': access_token},status=200)

        except Exception as e:
            return Response({'success':False, 'error': str(e)}, status=500)




    #list
    @api_view(['GET'])
    @require_token
    @require_token_admin
    def getAllUsers(request):
        try:
            user_objects = User.objects.all()
             
            #filtering
            filtered_data = userFilters(user_objects, request)
            
            #sorting
            sorted_data = sortHelper(filtered_data, request)

            #pagination
            response_data = paginationHelper(sorted_data, request, UserSerializer, SUCCESS_FETCHED_USERS)

           
            return Response(response_data, status=200)
        except Exception as e:
            return Response({'success': False, 'error': str(e)}, status=500)
            



    #retrive
    #need to write getone,update,delete
    @api_view(['GET'])
    @require_token
    def getOneUser(request):
        try:
            serializer = UserSerializer(request.user)

            return Response({'success': True, 'message': SUCCESS_FETCHED_USER, 'data': serializer.data},status=201)
        except User.DoesNotExist:
            return Response({'success' : False, 'error' : USER_NOT_FOUND}, status=404)
        except Exception as e:
            return Response({'success': False, 'error': str(e)}, status=500)
            



    #update
    @api_view(['PUT'])
    @require_token
    def updateUser(request):
        try:    
            user_details = request.user
            serializer = UserSerializer(user_details, data=request.data)
            if serializer.is_valid():
                serializer.save()

                return Response({'success': True, 'message': SUCCESS_UPDATED_USER, 'data': serializer.data},status=200)
            return Response({'success': False, 'error': serializer.errors}, status=422)
        except User.DoesNotExist as e:
            return Response({'success': False, 'error':USER_NOT_FOUND}, status=404)
        except Exception as e:
            return Response({'success': False,  'error': str(e)}, status=500)
        


       
        
    #delete
    @api_view(['DELETE'])
    @require_token
    def deleteUser(request):
        try:
            queryset = request.user
            queryset.delete()

            return Response({'success': True, 'message': SUCCESS_DELETED_USER},status=200)
        except User.DoesNotExist:
            return Response({'success': False, 'error': USER_NOT_FOUND}, status=404)
        except Exception as e:
            return Response({'success': False,  'error': str(e)}, status=500)
        



