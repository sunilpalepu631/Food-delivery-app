

def sortHelper(queryset, request):
    
    sort_by = request.query_params.get('sort_by', 'id').lower()
    sort_type = request.query_params.get('sort_type', 'desc').lower()

    if sort_type == 'desc':
        queryset = queryset.order_by(f'-{sort_by}')
    
    else:
        queryset = queryset.order_by(sort_by)

    return queryset

