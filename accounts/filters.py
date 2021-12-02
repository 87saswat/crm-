import django_filters
from django_filters import DateFilter, CharFilter
from .models import Order


class OrderFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name='date_created', lookup_expr='gte')
    end_date = DateFilter(field_name='date_created', lookup_expr='lte')
    product_search = CharFilter(field_name= 'product__name', lookup_expr='icontains')
    class Meta:
        model = Order
        fields = '__all__'