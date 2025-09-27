from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, get_object_or_404
from rest_framework.permissions import DjangoModelPermissions
from core.utils import SearchPagination
from yatra.filters import BusFilter
from yatra.serializers.bus import BusSerializer
from yatra.models.bus import Bus
from functools import partial

class BusFilterCreate(ListCreateAPIView):
    permission_classes = [DjangoModelPermissions]
    pagination_class = SearchPagination
    filterset_class = BusFilter
    filterset_fields = BusFilter.Meta.fields
    search_fields = BusFilter.fizzy_fields
    serializer_class = partial(BusSerializer, exclude=['metadata'])

    def get_queryset(self):
        return Bus.objects.filter(trip_id=self.kwargs.get('pk')).order_by('created_on')

    def get_serializer(self, *args, **kwargs):
        data = kwargs.get('data', None)
        if data:
            kwargs['data'] = data.copy()
            kwargs['data']['trip_id'] = self.kwargs.get('pk')
        return super().get_serializer(*args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class BusUD(APIView):
    permission_classes = [DjangoModelPermissions]
    queryset = Bus.objects.all()

    @staticmethod
    def patch(request, pk:int):
        """
        rename bus number
        """
        bus:Bus = get_object_or_404(Bus, pk=pk)
        new_no = request.data.get('number', None)
        if new_no:
            ser = BusSerializer(bus, data=request.data, fields=['number'])
            ser.is_valid(raise_exception=True)
            ser.save()

        return Response(BusSerializer(instance=bus).data)

    @staticmethod
    def delete(request, pk:int):
        bus:Bus = get_object_or_404(Bus, pk=pk)
        bus.delete()
        bus.save()

        return Response({'success_message': ['Bus deleted.']})

