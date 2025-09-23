from django.http import Http404
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.exceptions import NotAuthenticated, PermissionDenied
from rest_framework.views import exception_handler
import django_filters
from rest_framework.pagination import PageNumberPagination
from django.db import models

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        if isinstance(exc, (AuthenticationFailed, NotAuthenticated, PermissionDenied)):
            response.data = {'non_field_errors': [str(exc.detail)]}
            response.status_code = exc.status_code
        elif isinstance(exc, Http404):
            response.data = {'non_field_errors': [str(exc)]}

    return response

class BuildFilters:
    FIELD_TYPE_TO_FILTER = {
        models.CharField: django_filters.CharFilter,
        models.TextField: django_filters.CharFilter,
        models.IntegerField: django_filters.NumberFilter,
        models.AutoField: django_filters.NumberFilter,
        models.DecimalField: django_filters.NumberFilter,
        models.FloatField: django_filters.NumberFilter,
        models.BooleanField: django_filters.BooleanFilter,
        models.DateTimeField: django_filters.IsoDateTimeFilter,
        models.DateField: django_filters.DateFilter,
    }

    def __init__(self, model, exact_fields:list|None=None, fizzy_fields:list|None=None, date_fields:list|None=None):
        self.model = model
        self.exact_fields = exact_fields or []
        self.fizzy_fields = fizzy_fields or []
        self.date_fields = date_fields or []
        self.filter_fields = {}

    def get_field_type(self, dotted_field_name):
        parts = dotted_field_name.split('__')
        current_model = self.model
        for part in parts[:-1]:
            try:
                field = current_model._meta.get_field(part)
                if isinstance(field, models.ForeignKey):
                    current_model = field.related_model
                else:
                    return None
            except Exception:
                return None

        try:
            final_field = current_model._meta.get_field(parts[-1])
            return type(final_field)
        except Exception:
            return None

    def get_filter_class_for_field_type(self, field_type):
        for base_type, filter_class in self.FIELD_TYPE_TO_FILTER.items():
            if issubclass(field_type, base_type):
                return filter_class
        return django_filters.Filter  # fallback


    def build(self):
        # Fuzzy fields (icontains for strings)
        for field_name in self.fizzy_fields:
            field_type = self.get_field_type(field_name)
            if field_type:
                filter_class = self.get_filter_class_for_field_type(field_type)
                self.filter_fields[field_name] = filter_class(field_name=field_name, lookup_expr='icontains')

        # Exact match fields
        for field_name in self.exact_fields:
            field_type = self.get_field_type(field_name)
            if field_type:
                filter_class = self.get_filter_class_for_field_type(field_type)
                self.filter_fields[field_name] = filter_class(field_name=field_name, lookup_expr='exact')

        # Date fields: gte, lte
        for field_name in self.date_fields:
            field_type = self.get_field_type(field_name)
            if field_type and issubclass(field_type, (models.DateField, models.DateTimeField)):
                self.filter_fields[field_name + '__gte'] = django_filters.IsoDateTimeFilter(field_name=field_name, lookup_expr='gte')
                self.filter_fields[field_name + '__lte'] = django_filters.IsoDateTimeFilter(field_name=field_name, lookup_expr='lte')
                self.filter_fields[field_name + '__date'] = django_filters.DateFilter(field_name=field_name, lookup_expr='date')

        # Define Meta
        class Meta:
            model = self.model
            fields = list(self.filter_fields.keys())

        # Create FilterSet class dynamically
        filterset = type(
            f"{self.model.__name__}FilterSet",
            (django_filters.FilterSet,),
            {**self.filter_fields, 'Meta': Meta}
        )

        filterset.fizzy_fields = self.fizzy_fields
        return filterset

class SearchPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 120