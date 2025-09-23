from rest_framework.generics import CreateAPIView, ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from core.utils import SearchPagination
from yatra.models.trip import Trip
from rest_framework.permissions import DjangoModelPermissions
from yatra.serializers.trip import TripSerializer
from yatra.filters import TripFilter


class TripFilterCreate(ListCreateAPIView):
    permission_classes = [DjangoModelPermissions]
    pagination_class = SearchPagination
    filterset_class = TripFilter
    filterset_fields = TripFilter.Meta.fields
    search_fields = TripFilter.fizzy_fields
    serializer_class = TripSerializer
    queryset = Trip.objects.order_by('-created_on')

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class TripRUD(RetrieveUpdateDestroyAPIView):
    permission_classes = [DjangoModelPermissions]
    serializer_class = TripSerializer
    queryset = Trip.objects.all()