from rest_framework import serializers

from addresses.models import Address, Dong
from onepaper.serializers import ReadOnlyModelSerializer


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"


class DongSerializer(ReadOnlyModelSerializer):
    class Meta:
        model = Dong
        fields = "__all__"
