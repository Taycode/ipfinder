from rest_framework.serializers import ModelSerializer
from api.models import IPAddress


class IPAddressSerializer(ModelSerializer):
    class Meta:
        model = IPAddress
        fields = '__all__'


class IPAddressGetSerializer(ModelSerializer):
    class Meta:
        model = IPAddress
        fields = ['address', ]
