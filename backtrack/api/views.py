
from ..models import PBI
from . import serializers
from rest_framework import generics, status
from rest_framework.response import Response

class PBIListAndCreateView(generics.ListAPIView,generics.CreateAPIView):
    queryset = PBI.objects.all().order_by('priority')
    serializer_class = serializers.PBISerializer


    def update_priorities(self, inserting_priority):
        lower_priorities = PBI.objects.filter(priority__gte=inserting_priority)
        for item in lower_priorities:
            item.priority += 1
        lower_priorities.update()


    def create(self, request, *args, **kwargs):
        inserting_priority = request.data['priority']
        self.update_priorities(inserting_priority)
        super(PBIListAndCreateView, self).create(request, args, kwargs)
        response = {"status_code": status.HTTP_201_CREATED,
                    "message": "Successfully created",
                    "result": request.data}
        return Response(response)

class PBIDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PBI.objects.all()
    serializer_class = serializers.PBISerializer

    def retrieve(self, request, *args, **kwargs):
        super(PBIDetailView, self).retrieve(request, args, kwargs)
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        response = {"status_code": status.HTTP_200_OK,
                    "message": "Successfully retrieved",
                    "result": data}
        return Response(response)

    def patch(self, request, *args, **kwargs):
        super(PBIDetailView, self).patch(request, args, kwargs)
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        response = {"status_code": status.HTTP_200_OK,
                    "message": "Successfully updated",
                    "result": data}
        return Response(response)

    def delete(self, request, *args, **kwargs):
        super(PBIDetailView, self).delete(request, args, kwargs)
        response = {"status_code": status.HTTP_200_OK,
                    "message": "Successfully deleted"}
        return Response(response)


