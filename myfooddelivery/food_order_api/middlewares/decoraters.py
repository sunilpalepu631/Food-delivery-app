import jwt
from functools import wraps
from rest_framework.response import Response
from django.conf import settings
from rest_framework import exceptions
from ..constants.messages import *
from ..models import User




#for user
def require_token(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            # raise exceptions.AuthenticationFailed('authentication failed')  
            return Response({'success': False, 'error': TOKEN_REQUIRED}, status=401)
        
        try:
            decoded_data = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms=['HS256'])
            user_id = decoded_data['user_id']

            user = User.objects.get(id=user_id)
            request.user = user
            
            return view_func(request, *args, **kwargs)

        except jwt.ExpiredSignatureError:
            return Response({'success':False, 'error': TOKEN_EXPIRED}, status=401)
        except User.DoesNotExist:
            return Response({'success':False, 'error': USER_NOT_FOUND}, status=404)
        except Exception as e:
            return Response({'success': False, 'error' : INVALID_TOKEN}, status=401)

    return _wrapped_view

    

#for admin
def require_token_admin(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        try:
            user_details = request.user
            
            if user_details.user_type != 'ADMIN':
                return Response({'success': False, 'error': USER_NOT_ALLOWED},status=403)
                
            return view_func(request, *args, **kwargs)
        except Exception as e:
            return Response({'success': False, 'error': str(e)}, status=500)

    return _wrapped_view

