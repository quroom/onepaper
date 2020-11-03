from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from addresses.models import Address
from addresses.serializers import AddressSerializer
from papers.permissions import 

class AddressModelViewSet(ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer