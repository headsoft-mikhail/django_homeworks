from django_filters import rest_framework as filters, DateTimeFilter

from advertisements.models import Advertisement


class AdvertisementFilter(filters.FilterSet):
    """Фильтры для объявлений."""
    created_at_after = DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_at_before = DateTimeFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = Advertisement
        fields = ['creator', 'status', 'created_at_after', 'created_at_before']

