from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer, CharField
from core.utils.serializers import ModelSerializer
from manufacturing.models import WorkCenter

class WorkCenterSerializer(ModelSerializer):
    class Meta:
        model = WorkCenter
        exclude = ['company', 'create_date', 'update_date']

    working_state = CharField(read_only=True)
    status = CharField(read_only=True)