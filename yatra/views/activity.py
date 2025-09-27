from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response
from yatra.filters import ActivityFilter
from yatra.serializers.activity import ActivitySerializer
from core.utils import SearchPagination
from yatra.models.activity import Activity
from yatra.permissions import CanUpdateActivity
from rest_framework.exceptions import ValidationError
from django.utils import timezone


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

class ActivityRUD(RetrieveUpdateDestroyAPIView):
    permission_classes = [DjangoModelPermissions]
    serializer_class = ActivitySerializer
    queryset = Activity.objects.all()

@api_view(['PATCH'])
@permission_classes([CanUpdateActivity])
def start_activity(request, pk:int):
    act:Activity = get_object_or_404(Activity, pk=pk)
    if not act.trip.started:
        raise ValidationError({'non_field_error': ['Start the trip to start its activities.']})
    if act.started:
        raise ValidationError({'non_field_error': ['Activity already started.']})

    act.started_on = timezone.now()
    act.started = True
    act.save()

    return Response(ActivitySerializer(instance=act).data)

@api_view(['PATCH'])
@permission_classes([CanUpdateActivity])
def end_activity(request, pk:int):
    act:Activity = get_object_or_404(Activity, pk=pk)

    if not act.started:
        raise ValidationError({'non_field_error': ['Start activity to end it.']})
    if act.ended:
        raise ValidationError({'non_field_error': ['Activity already ended.']})

    act.ended = True
    act.ended_on = timezone.now()
    act.save()

    return Response(ActivitySerializer(instance=act).data)