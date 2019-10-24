from ..models import PBI
from rest_framework import serializers


class PBISerializer(serializers.ModelSerializer):
    class Meta:
        model = PBI
        fields = ('name', 'description', 'priority', 'estimate' ,'status', 'id')  # if not declared, all fields of the model will be shown

