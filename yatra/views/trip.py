from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404, ListAPIView
from rest_framework.response import Response
from core.utils import SearchPagination
from yatra.models.trip import Trip, UserTrip
from rest_framework.permissions import DjangoModelPermissions
from yatra.serializers.trip import TripSerializer
from yatra.filters import TripFilter
from yatra.permissions import CanUpdateTrip, AssignTripToUser
from rest_framework.exceptions import ValidationError
from django.utils import timezone
from yatra.models.user import User
from yatra.serializers.trip import UserTripSerializer
from yatra.filters import UserTripFilter

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

class UserTripListCreate(ListAPIView):
    serializer_class = UserTripSerializer
    permission_classes = [DjangoModelPermissions]
    pagination_class = SearchPagination
    filterset_class = UserTripFilter
    filterset_fields = UserTripFilter.Meta.fields
    search_fields = UserTripFilter.fizzy_fields

    def get_queryset(self):
        return UserTrip.objects.filter(trip_id=self.kwargs.get('pk'))

    def get_permissions(self):
        """Use different permission for POST vs GET"""
        if self.request.method == "POST":
            return [AssignTripToUser()]
        return super().get_permissions()

    @staticmethod
    def post(request, pk:int):
        trip = get_object_or_404(Trip, pk=pk)

        u = set(request.data.get('users'))
        u = list(User.objects.filter(id__in=u).exclude(user_trips__trip=trip))

        objs = [UserTrip(created_by=request.user, user=i, trip=trip) for i in u]
        UserTrip.objects.bulk_create(objs)
        objs = UserTrip.objects.filter(trip=trip, user__in=u).prefetch_related('user', 'created_by', 'trip')

        return Response(UserTripSerializer(instance=objs, many=True, exclude=['checked_in', 'checked_in_on']).data)