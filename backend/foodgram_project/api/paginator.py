from rest_framework.pagination import PageNumberPagination


class LimitPageNumberPagination(PageNumberPagination):
    """Класс для переопределения атрибута."""

    page_size_query_param = 'limit'
