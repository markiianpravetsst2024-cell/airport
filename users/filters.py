import django_filters
from .models import User

class UserFilter(django_filters.FilterSet):
    role_name = django_filters.CharFilter(method='filter_role')

    class Meta:
        model = User
        fields = []

    def filter_role(self, queryset, name, value):
        return queryset.filter(role=value)
