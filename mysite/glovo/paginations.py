from rest_framework.pagination import PageNumberPagination

class StorePagination(PageNumberPagination):
    page_size = 4


class CategoryPagination(PageNumberPagination):
    page_size = 2


class ProductPagination(PageNumberPagination):
    page_size = 3