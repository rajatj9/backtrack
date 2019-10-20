
from ..models import PBI
from . import serializers
from rest_framework import generics, status
from rest_framework.response import Response

class PBIListView(generics.ListAPIView):
    queryset = PBI.objects.all()
    serializer_class = serializers.PBISerializer

