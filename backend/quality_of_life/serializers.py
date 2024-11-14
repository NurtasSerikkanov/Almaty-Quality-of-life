# serializers.py
from rest_framework import serializers
from .models import Appeal, ExecutionInfo, ResponseInfo, AdditionalAttributes

class ExecutionInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExecutionInfo
        fields = '__all__'


class ResponseInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResponseInfo
        fields = '__all__'


class AdditionalAttributesSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalAttributes
        fields = '__all__'


class AppealSerializer(serializers.ModelSerializer):
    executions = ExecutionInfoSerializer(many=True, read_only=True)
    responses = ResponseInfoSerializer(many=True, read_only=True)
    attributes = AdditionalAttributesSerializer(many=True, read_only=True)

    class Meta:
        model = Appeal
        fields = ['id', 'title', 'description', 'creation_date', 'completion_date',
                  'status', 'process_status', 'address', 'coord_x', 'coord_y',
                  'location', 'hexagon_id',
                  'executions', 'responses', 'attributes', 'boundary_coords']

