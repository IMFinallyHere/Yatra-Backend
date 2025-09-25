from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import DjangoModelPermissions
from yatra.filters import ActivityFilter
from yatra.serializers.activity import ActivitySerializer
from core.utils import SearchPagination
from yatra.models.activity import Activity


class ActivityFilterCreate(ListCreateAPIView):
    permission_classes = [DjangoModelPermissions]
    pagination_class = SearchPagination
    filterset_class = ActivityFilter
    filterset_fields = ActivityFilter.Meta.fields
    search_fields = ActivityFilter.fizzy_fields
    serializer_class = ActivitySerializer

    def get_queryset(self):
        return Activity.objects.filter(trip_id=self.kwargs.get('pk')).order_by('-created_on')

    def get_serializer(self, *args, **kwargs):
        data = kwargs.get('data', None)
        if data:
            kwargs['data'] = data.copy()
            kwargs['data']['trip_id'] = self.kwargs.get('pk')
        return super().get_serializer(*args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

