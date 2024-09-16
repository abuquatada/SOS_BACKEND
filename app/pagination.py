from rest_framework.pagination import PageNumberPagination

class Userpagination(PageNumberPagination):
    page_size=2
    page_query_param='page'
    page_size_query_param='size'
    


    
