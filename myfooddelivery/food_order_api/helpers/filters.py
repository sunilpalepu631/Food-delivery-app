from ..models import *



def userFilters(user_objects, request):

    query = request.query_params
    user = user_objects

    if 'username' in query:
        user = user.filter(username__startswith=query.get('username'))

    if 'first_name' in query:
        user = user.filter(first_name__startswith=query.get('first_name'))

    if 'last_name' in query:
        user = user.filter(last_name__startswith=query.get('last_name'))

    if 'user_type' in query:
        user = user.filter(user_type__startswith=query.get('user_type'))

    return user




def RestaurantFilter(restaurant_data, request):
    restaurant = restaurant_data
    query = request.query_params

    if 'search' in query:
        restaurant = restaurant.filter(name__icontains=query.get('search'))

    if 'restaurant_type' in query:
        print(query.get('restaurant_type').lower())
        restaurant = restaurant.filter(type_of_restaurant=query.get('restaurant_type').upper())

    return restaurant





def FoodItemFilter(food_items_data, request):
    food_item = food_items_data
    query = request.query_params

    if 'name' in query:
        food_item = food_item.filter(name__icontains=query.get('name'))

    if 'food_type' in query:
        food_item = food_item.filter(food_type__startswith=query.get('food_type'))

    if 'restaurant_name' in query:
        food_item = food_item.filter(restaurant__name__startswith=query.get('restaurant_name'))

    if 'price_greater_then' in query:
        food_item = food_item.filter(price__gte=query.get('price_greater_then'))

    if 'price_less_then' in query:
        food_item = food_item.filter(price__lte=query.get('price_less_then'))

    return food_item

    
    


def OrderFilter(order_data, request):
    order = order_data
    query = request.query_params

    if 'user' in query:
        order = order.filter(user__username__startswith=query.get('user'))

    if 'restaurant' in query:
        order = order.filter(restaurant__name__startswith=query.get('restaurant'))

    if 'order_date' in query:
        order = order.filter(ordered_date__range=(query.get('order_date'), query.get('order_date')))

    if 'delivery_person' in query:
        order = order.filter(delivery_person__first_name__startswith=query.get('delivery_person'))

    if 'total_price_greater_then' in query:
        order = order.filter(total_price__gte=query.get('total_price_greater_then'))

    if 'total_price_less_then' in query:
        order = order.filter(total_price__lte=query.get('total_price_less_then'))

    if 'status' in query:
        print('in status', query.get('status').upper())
        order = order.filter(status=query.get('status').upper())
    
    return order




def logFilters(log_data, request):
    query = request.query_params

    if 'order_id' in query:
        log_data = log_data.filter(order=query.get('order_id'))
    if 'user_id' in query:
        log_data = log_data.filter(user=query.get('user_id'))
    if 'order_status' in query:
        log_data = log_data.filter(order_status=query.get('order_status').upper())

        
    return log_data




def DeliveryPersonFilter(delivery_person_data, request):
    delivery_person = delivery_person_data
    query = request.query_params

    if 'delivery_person_name' in query:
        delivery_person = delivery_person.filter(first_name__startswith=query.get('delivery_person_name'))

    if 'delivery_person_email' in query:
        delivery_person = delivery_person.filter(email__startswith=query.get('delivery_person_email'))


    return delivery_person

