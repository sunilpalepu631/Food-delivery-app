from django.contrib import admin
from django.urls import path, include
from  ..controller.userControllers import UserViews


urlpatterns = [
    path('', UserViews.getAllUsers),

    path('registeruser/', UserViews.registerUser),
    path('login/', UserViews.loginUser),
    path('getaccesstoken/', UserViews.getAccessToken),
    
    path('myprofile/', UserViews.getOneUser),
    path('me/update/', UserViews.updateUser),
    path('me/delete/', UserViews.deleteUser),
]

