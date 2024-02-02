import json
from django.conf import settings
from django.shortcuts import render

import razorpay
from rest_framework.decorators import api_view
from rest_framework.response import Response

from ..models import Order
from ..serializers.ordersSerializer import *



@api_view(['POST'])
def start_payment(request):
    # request.data is coming from frontend
    order_id = request.data.get('order_id')

    # public_key = env('PUBLIC_KEY')
    # secret_key = env('SECRET_KEY')
    public_key = settings.PUBLIC_KEY
    secret_key = settings.SECRET_KEY

    client = razorpay.Client(auth=(public_key, secret_key))

    # create razorpay order
    # the amount will come in 'paise' that means if we pass 50 amount will become
    # 0.5 rupees that means 50 paise so we have to convert it in rupees. So, we will 
    # mumtiply it by 100 so it will be 50 rupees.
    order = Order.objects.get(id=order_id)
    amount = order.total_price
    print(amount)

    payment = client.order.create(
        {
            'amount' : int(amount) * 100,
            'currency' : 'INR',
            'payment_capture' : '1'
        }
    )
    print('****************')
    print(payment)
    print('****************')


    order.order_payment_id = payment['id']
    order.save()

    # serializer = GetOrderSerializer(order)



    context = {
       'order_id': payment['id'],
       'amount': amount
   }
    return render(request, 'payment.html', context)



    # data = {
    #     "payment": payment,
    #     "order": serializer.data
    # }
    # return Response(data)



@api_view(['POST'])
def handle_payment_success(request):
    # request.data is coming from frontend
    res = json.loads(request.data["response"])

   

    order = Order.objects.get(order_payment_id=res['razorpay_order_id'])

    # we will pass this whole data in razorpay client to verify the payment
    data = {
        'razorpay_order_id': res['razorpay_order_id'],
        'razorpay_payment_id': res['razorpay_order_id'],
        'razorpay_signature': res['razorpay_signature']
    }

    #veryfying signature
    client = razorpay.Client(auth=(settings.PUBLIC_KEY, settings.SECRET_KEY))
    try:
        status = client.utility.verify_payment_signature(data)
        order.payment_status = True
        order.save()
        return Response({'message': 'Payment Successful '})
    except:
        return Response({'error': 'Payment Failure'})





client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET_KEY))

def initiate_payment(amount, currency='INR'):
    data = {
       'amount': amount * 100,  # Razorpay expects amount in paise (e.g., 100 INR = 10000 paise)
       'currency': currency,
       'payment_capture': '1'  # Auto capture the payment after successful authorization
   }
    response = client.order.create(data=data)
    return response['id']





@api_view(['POST'])
def payment_view(request):
   id = request.data.get('id')
   print('id')
   order = Order.objects.get(id=id)
   amount = order.total_price
   amount = amount  # Set the amount dynamically or based on your requirements

   order_id = initiate_payment(amount)
   context = {
       'order_id': order_id, #order_id means in razorpay order_id
       'amount': amount
   }
   return render(request, 'payment.html', context)


@api_view(['POST'])
def payment_success_view(request):
   order_id = request.data.get('order_id')
   payment_id = request.data.get('razorpay_payment_id')
   signature = request.data.get('razorpay_signature')
   params_dict = {
       'razorpay_order_id': order_id,
       'razorpay_payment_id': payment_id,
       'razorpay_signature': signature
   }
   try:
       client.utility.verify_payment_signature(params_dict)
       # Payment signature verification successful
       # Perform any required actions (e.g., update the order status)
       return Response('Payment success')
   except razorpay.errors.SignatureVerificationError as e:
       # Payment signature verification failed
       # Handle the error accordingly
       return Response('Payment Failed')