from rest_framework.pagination import PageNumberPagination


class LimitPageNumberPagination(PageNumberPagination):
    """Класс для переопределения атрибута пагинациии page_size_query_param."""

    page_size_query_param = 'limit'
