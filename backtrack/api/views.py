
from ..models import PBI
from . import serializers
from rest_framework import generics, status
from rest_framework.response import Response

class PBIListView(generics.ListAPIView):
    queryset = PBI.objects.all()
    serializer_class = serializers.PBISerializer

class PBICreateView(generics.CreateAPIView):
    queryset = PBI.objects.all()
    serializer_class = serializers.PBISerializer

    def create(self, request, *args, **kwargs):
        super(PBICreateView, self).create(request, args, kwargs)
        response = {"status_code": status.HTTP_200_OK,
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
