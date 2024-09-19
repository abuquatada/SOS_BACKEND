from rest_framework.pagination import LimitOffsetPagination,CursorPagination,PageNumberPagination
from rest_framework.response import Response

class CustomPagination(PageNumberPagination):    
    def __init__(self,given_size=25):
        self.page_size = given_size
        
    def get_paginated_response(self, data):
        print(f'\n\n\nThis is data {data}')
        count = self.page.paginator.count
        total_page=self.page.paginator.num_pages
        print('\n\n\n',f'total pages {total_page}','\n\n\n')
        return Response(
            {
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            "total_page":total_page,
            "result":data
        }
                    )
        
        
class Userpagination(PageNumberPagination):
    page_size=2
    page_query_param='page'
    page_size_query_param='size'
            