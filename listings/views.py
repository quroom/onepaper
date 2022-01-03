import django_filters
from django.db.models.base import Model
from django.shortcuts import render
from django_filters import rest_framework as filters
from django_filters.rest_framework import BaseInFilter, NumberFilter
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# Create your views here.
from rest_framework.viewsets import ModelViewSet

from listings.models import Listing
from listings.permissions import HasProfileOrReadonly
from listings.serializers import ListingEveryoneSerializer, ListingSerializer
from papers.permissions import IsAuthorOrReadonly


class _NumberInFilter(BaseInFilter, NumberFilter):
    pass


class ListingFilter(django_filters.FilterSet):
    bjdong = django_filters.CharFilter(
        lookup_expr="icontains", field_name="listingaddress__bjdongName"
    )
    max_deposit = filters.NumberFilter(field_name="deposit", lookup_expr="lte")
    min_deposit = filters.NumberFilter(field_name="deposit", lookup_expr="gte")
    max_monthly_fee = filters.NumberFilter(field_name="monthly_fee", lookup_expr="lte")
    min_monthly_fee = filters.NumberFilter(field_name="monthly_fee", lookup_expr="gte")
    item_category = _NumberInFilter()
    trade_category = _NumberInFilter()

    class Meta:
        model = Listing
        fields = [
            "item_category",
            "bjdong",
            "max_deposit",
            "min_deposit",
            "max_monthly_fee",
            "min_monthly_fee",
            "trade_category",
        ]


class ListingViewset(ModelViewSet):
    permission_classes = [IsAuthenticated, HasProfileOrReadonly, IsAuthorOrReadonly]
    serializer_class = ListingSerializer
    queryset = Listing.objects.all()
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    filter_class = ListingFilter

    def get_serializer_class(self):
        is_mine = self.request.query_params.get("is_mine", None)
        if self.action == "list":
            if is_mine:
                return ListingSerializer
            else:
                return ListingEveryoneSerializer
        else:
            return ListingSerializer

    def list(self, request, *args, **kwargs):
        is_mine = request.query_params.get("is_mine", None)
        queryset = self.filter_queryset(self.get_queryset())

        if is_mine:
            queryset = queryset.filter(author=request.user)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author == request.user:
            serializer = self.get_serializer(instance)
        else:
            serializer = ListingEveryoneSerializer(instance)

        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
