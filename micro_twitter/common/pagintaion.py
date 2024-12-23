from rest_framework import pagination


class SmallResultsSetLimitOffsetPagination(pagination.LimitOffsetPagination):
    default_limit = 5
    max_limit = 10
