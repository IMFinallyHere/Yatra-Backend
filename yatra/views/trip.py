from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import CreateAPIView, ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework.response import Response

from core.utils import SearchPagination
from yatra.models.trip import Trip
from rest_framework.permissions import DjangoModelPermissions
from yatra.serializers.trip import TripSerializer
from yatra.filters import TripFilter
from yatra.permissions import CanUpdateTrip
from rest_framework.exceptions import ValidationError
from django.utils import timezone

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

@api_view(['PATCH'])
@permission_classes([CanUpdateTrip])
def start_trip(request, pk:int):
    trip:Trip = get_object_or_404(Trip, pk=pk)

    if trip.started:
        raise ValidationError({'non_field_error': ['Trip already started.']})

    trip.started = True
    trip.started_on = timezone.now()
    trip.save()

    return Response(TripSerializer(instance=trip).data)

@api_view(['PATCH'])
@permission_classes([CanUpdateTrip])
def end_trip(request, pk:int):
    trip:Trip = get_object_or_404(Trip, pk=pk)

    if not trip.started:
        raise ValidationError({'non_field_error': ['Start trip to end it.']})
    if trip.ended:
        raise ValidationError({'non_field_error': ['Trip already ended.']})

    trip.ended = True
    trip.ended_on = timezone.now()
    trip.save()

    return Response(TripSerializer(instance=trip).data)