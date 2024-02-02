import re
from rest_framework import serializers
from ..models import User
from django.contrib.auth.hashers import make_password
from rest_framework.validators import ValidationError
from ..constants.messages import *




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
       

        extra_kwargs = {
            'username': {
                'error_messages': {
                    # "required": "username fileds should be required",
                    'blank': 'username should not be empty',
                    'min_length':'minimum 6 characters length required'
                }
            },
            'password': {
                'write_only': True,
                'error_messages': {
                    'blank': 'password should not be blank',
                    'min_length':'minimum 6 characters length required'
                }
            }
        }


    def validate_password(self, value):

        

        if not any(char.isdigit() for char in value):
                raise ValidationError(ATLEAST_ONE_NUMBER)

        if not any(char.isupper() for char in value):
            raise ValidationError(ATLEAST_ONE_UPPERCASE)

        if not any(char.islower() for char in value):
            raise ValidationError(ATLEAST_ONE_LOWERCASE)

        if not re.findall(r'[!@#$%^&*]', value):
            raise ValidationError(ATLEAST_ONE_SPECIAL_CHARACTER)

        return value



    def create(self, validated_data):
        # Manually hash the password before saving
        password = validated_data['password']

        validated_data['password'] = make_password(password)
        
        user =  super(UserSerializer, self).create(validated_data)

        return user


    
    def update(self, instance, validated_data):
        # Manually hash the password before updating
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])

        return super(UserSerializer, self).update(instance, validated_data)
    
        


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

