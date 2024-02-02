from django.contrib import admin
from django.urls import path, include
from  ..controller.orderControllers import OrdersView
from ..controller.payment import *

urlpatterns = [

    path('payment/', payment_view, name='payment'),
    path('payment/success/', payment_success_view, name='payment_success'),


    path('', OrdersView.getallOrders),
    path('add', OrdersView.addOrder),

    path('start-payment', start_payment),
    path('start-payment/success/', handle_payment_success),

    path('simulate-payment/<int:order_id>', OrdersView.simulatePaymentView),
    path('accepted/<int:order_id>', OrdersView.accepted),
    path('dispatched/<int:order_id>', OrdersView.dispatched),
    path('delivered/<int:order_id>', OrdersView.delivered),

    path('listlogs/', OrdersView.getAllLogs),

    path('<int:id>', OrdersView.getOneOrder),
    path('myorders/', OrdersView.getMyOrders),

    path('update/<int:id>', OrdersView.updateOrder),
    path('delete/<int:id>', OrdersView.deleteOrder),
]

