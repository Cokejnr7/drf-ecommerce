from rest_framework import filters


class PriceRangeFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        # get the min_price and max_price query parameters from request
        min_price = request.query_params.get("min_price")
        max_price = request.query_params.get("max_price")

        # check if min_price is provided
        if min_price is not None:
            # filter products with price greater than or equal to min_price
            queryset = queryset.filter(price__gte=min_price)

        # checks if max_price is provided
        if max_price is not None:
            # filter products with price less than or equal to max_price
            queryset = queryset.filter(price__lte=max_price)

        return queryset
