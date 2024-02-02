import random
from django.db import models
from django.core.validators import MinLengthValidator, RegexValidator



class User(models.Model):
    TYPE_CHOICES = [
        ('USER', 'user'),
        ('ADMIN', 'admin')
    ]
    username = models.CharField(max_length=15, validators=[MinLengthValidator(limit_value=6)],unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255, validators=[MinLengthValidator(limit_value=6)])
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    user_type = models.CharField(max_length=255,choices=TYPE_CHOICES, default='USER')

    phone_number_validator = RegexValidator(regex=r'^\d+$', message='Phone number must contain only numeric digits.')
    phone_number = models.CharField(max_length=10, unique=True, validators=[MinLengthValidator(limit_value=10), phone_number_validator])
    address = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
   

    def __str__(self):
        return self.email



class Restaurant(models.Model):

    TYPE_CHOICES = [
        ('VEG', 'vegetarian'),
        ('NON_VEG', 'non_vegetarian'),
        ('VEG_AND_NON_VEG', 'veg_and_non_veg')
    ]
    phone_number_validator = RegexValidator(
        regex=r'^\d+$', message='Phone number must contain only numeric digits.')


    name = models.CharField(max_length=255, unique=True)
    type_of_restaurant = models.CharField(max_length=255, choices=TYPE_CHOICES,  default='VEG_AND_NON_VEG')
    address = models.TextField()
    phone_number = models.CharField(max_length=10, unique=True, validators=[MinLengthValidator(limit_value=10), phone_number_validator])
    

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name



class FoodItem(models.Model):
   
    FOOD_TYPE_CHOICES = [
        ('VEG', 'Vegetarian'),
        ('NON_VEG', 'Non-Vegetarian'),
    ]
    
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    food_type = models.CharField(
        max_length=50,
        choices=FOOD_TYPE_CHOICES,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('restaurant', 'name')
        

   
    def __str__(self):
        return f'{self.restaurant.name} {self.name}'



class DeliveryPerson(models.Model):
    email = models.EmailField(default = 'sample@example.com')
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number_validator = RegexValidator(regex=r'^\d+$', message='Phone number must contain only numeric digits.')
    phone_number = models.CharField(max_length=10, unique=True, validators=[MinLengthValidator(limit_value=10), phone_number_validator])

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.first_name


    

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    items = models.JSONField()
    total_price = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    
    # #payment status
    payment_status_type = models.TextChoices('payment_status', 'SUCCESS PENDING FAILURE')
    payment_status = models.CharField(max_length=254, choices=payment_status_type.choices, default='PENDING')

    payment_date = models.DateTimeField(null=True, blank=True)
    provider_order_id = models.CharField(max_length=255, default='')
    payment_id = models.CharField(max_length=254)
    signature_id = models.CharField('signature ID', max_length=254)

    #order status
    status_type = models.TextChoices("status_type", "PAYMENT_PENDING PAYMENT_DONE ACCEPTED CANCELLED DISPATCHED DELIVERED")
    status = models.CharField(max_length=50, choices=status_type.choices, default='PAYMENT_PENDING')
    
    ordered_date = models.DateTimeField(auto_now_add=True)

    #Delivery person
    delivery_person = models.ForeignKey(DeliveryPerson, on_delete=models.CASCADE, null=True, blank=True)
    delivery_status = models.BooleanField(default=False)
    delivered_date = models.DateTimeField(null=True, blank=True)

    
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email}'s order_number {str(self.id)}"



class Logs(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    status_type = models.TextChoices("status_type", "PAYMENT_PENDING PAYMENT_DONE ACCEPTED CANCELLED DISPATCHED DELIVERED")
    order_status = models.CharField(max_length=50, choices=status_type.choices)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


