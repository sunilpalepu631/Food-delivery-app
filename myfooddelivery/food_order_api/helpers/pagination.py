import math
from rest_framework.pagination import PageNumberPagination



def paginationHelper(sorted_data, request, required_serializer, success_message):

    paginator = PageNumberPagination()

    paginator.page_size = limit = int(request.query_params.get('limit', 10 ))
    page = int(request.query_params.get('page', 1))

    result_page = paginator.paginate_queryset(sorted_data, request)

    serialized_data = required_serializer(result_page, many=True)
    count = paginator.page.paginator.count

    #new
    totalPages = math.ceil(count/limit)

    next_page = None
    if page < totalPages:
        next_page = page + 1
    else:
        next_page = None
    previous_page = None

    if page > 1:
        previous_page = page - 1
    else:
        previous_page = None


    response_data = {
        'success': True,
        'message': success_message,
        "count" : count,
        'total_pages' : totalPages,
        'current_page' : page,
        'results_per_page':limit,
        'next_page': next_page,
        'previous_page':previous_page,
        'data' : serialized_data.data
    }
    return response_data





#     response_data = pagination(success_message, count, limit, page, serialized_data.data)
    
#     return response_data



# def pagination(message, count, limit, page, Data):

#     totalPages = math.ceil(count/limit)

#     next_page = None
#     if page < totalPages:
#         next_page = page + 1
#     else:
#         next_page = None
#     previous_page = None

#     if page > 1:
#         previous_page = page - 1
#     else:
#         previous_page = None


#     response_data = {
#         'success': True,
#         'message': message,
#         "count" : count,
#         'total_pages' : totalPages,
#         'current_page' : page,
#         'results_per_page':limit,
#         'next_page': next_page,
#         'previous_page':previous_page,
#         'data' : Data
#     }
#     return response_data

