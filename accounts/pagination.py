from rest_framework.pagination import PageNumberPagination


class StaffDriverPaginator(PageNumberPagination):
    
    page_query_param = 'p'
    page_size = 1
    page_size_query_param = 'page_size'
    max_page_size = 1
    
class CustomerPaginator(PageNumberPagination):
    
    page_query_param = 'p'
    page_size = 1
    page_size_query_param = 'page_size'
    max_page_size = 1