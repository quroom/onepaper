from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from addresses.models import Address, Dong
from addresses.serializers import AddressSerializer, DongSerializer


class AddressModelViewSet(ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer


class DongAPIView(APIView):
    def get(self, request):
        # FIXME: 모든 법정동으로 바꾸기, 현재는 광주지역만 매물문의를 받을거라 이렇게 해둠.
        dongs = Dong.objects.filter(name__contains="광주광역시")
        serializer = DongSerializer(dongs, many=True)
        return Response(serializer.data)
