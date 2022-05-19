import datetime

import django_filters
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _
from django_filters import rest_framework as filters
from django_filters.rest_framework import BaseInFilter, NumberFilter
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.
from rest_framework.viewsets import ModelViewSet

from listings.models import AskListing, Listing, ListingItem, ListingStatus, ListingVisit
from listings.serializers import (
    AskListingSerializer,
    ListingDetailEveryoneSerializer,
    ListingEveryoneSerializer,
    ListingSerializer,
    ListingVisitDetailSerializer,
    ListingVisitSerializer,
)
from papers.permissions import HasProfileIsAuthorOrReadonly, IsAuthor
from profiles.models import ExpertProfile, Profile


class _NumberInFilter(BaseInFilter, NumberFilter):
    pass


class ListingFilter(django_filters.FilterSet):
    bjdong = django_filters.CharFilter(
        lookup_expr="icontains", field_name="listingaddress__bjdongName"
    )
    max_security_deposit = filters.NumberFilter(field_name="security_deposit", lookup_expr="lte")
    min_security_deposit = filters.NumberFilter(field_name="security_deposit", lookup_expr="gte")
    max_monthly_fee = filters.NumberFilter(field_name="monthly_fee", lookup_expr="lte")
    min_monthly_fee = filters.NumberFilter(field_name="monthly_fee", lookup_expr="gte")
    max_maintenance_fee = filters.NumberFilter(field_name="maintenance_fee", lookup_expr="lte")
    min_maintenance_fee = filters.NumberFilter(field_name="maintenance_fee", lookup_expr="gte")
    item_category = _NumberInFilter()
    trade_category = _NumberInFilter()

    class Meta:
        model = Listing
        fields = [
            "bjdong",
            "max_security_deposit",
            "min_security_deposit",
            "max_monthly_fee",
            "min_monthly_fee",
            "max_maintenance_fee",
            "min_maintenance_fee",
            "item_category",
            "trade_category",
        ]


class AskListingViewset(ModelViewSet):
    permission_classes = [IsAuthenticated, HasProfileIsAuthorOrReadonly]
    serializer_class = AskListingSerializer

    def get_queryset(self):
        queryset = AskListing.objects.all()

        approved_expert = Profile.objects.filter(
            user=self.request.user,
            expert_profile__status=ExpertProfile.APPROVED,
            is_activated=True,
        ).exists()

        if not approved_expert:
            queryset = queryset.filter(author=self.request.user)

        return queryset

    def list(self, request, *args, **kwargs):
        location = request.query_params.get("location", None)
        queryset = self.filter_queryset(self.get_queryset())
        if location:
            queryset = queryset.filter(location__contains=location)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ListingViewset(ModelViewSet):
    permission_classes = [IsAuthenticated, HasProfileIsAuthorOrReadonly]
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
        only_vacancy = request.query_params.get("only_vacancy", None)
        queryset = self.filter_queryset(self.get_queryset())
        now = datetime.datetime.utcnow()
        if is_mine:
            queryset = queryset.filter(author=request.user)
        if only_vacancy:
            queryset = queryset.filter(
                Q(available_date__lte=now) | Q(listingitem__available_date__lte=now)
            ).distinct()

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
            serializer = ListingDetailEveryoneSerializer(instance, context={"request": request})

        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ListingVisitCreateAPIView(generics.CreateAPIView):
    queryset = ListingVisit.objects.all()
    serializer_class = ListingVisitSerializer
    permission_classes = [IsAuthenticated, HasProfileIsAuthorOrReadonly]

    def perform_create(self, serializer):
        request_user = self.request.user
        pk = self.kwargs.get("pk")
        listing_item_id = self.request.data.get("listing_item_id")
        if listing_item_id:
            listing_item = get_object_or_404(ListingItem, id=listing_item_id)
            if listing_item.listing_item_visits.filter(author=request_user).exists():
                raise ValidationError({"detail": _("You have already asked.")})
            serializer.save(
                author=request_user, listing=listing_item.listing, listing_item=listing_item
            )
        else:
            listing = get_object_or_404(Listing, pk=pk)
            if listing.listingitem_set.exists():
                raise ValidationError({"detail": _("Submit with room.")})

            if listing.listing_visits.filter(author=request_user).exists():
                raise ValidationError({"detail": _("You have already asked.")})
            serializer.save(author=request_user, listing=listing)


class ListingVisitDestoryAPIView(generics.DestroyAPIView):
    # FIXME: Support Update method. I guess retrieve is not necessary. Beacuse it return all values in list.

    queryset = ListingVisit.objects.all()
    serializer_class = ListingVisitSerializer
    permission_classes = [IsAuthenticated, IsAuthor]


class ListingVisitListAPIView(generics.ListAPIView):
    serializer_class = ListingVisitDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = ListingVisit.objects.filter(author=self.request.user).order_by(
            "-updated_at"
        ) | ListingVisit.objects.filter(listing__author=self.request.user).order_by("-updated_at")
        location = self.request.query_params.get("location", None)
        if location:
            queryset = queryset.filter(listing__listingaddress__old_address__contains=location)
        return queryset


class ListingStatusAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAuthor]

    def put(self, request, pk):
        listingstatus = get_object_or_404(ListingStatus, listing__id=pk)
        self.check_object_permissions(self.request, listingstatus.listing)
        listing_status = request.data.get("status")

        listingstatus.status = listing_status
        listingstatus.save()

        return Response({"status": int(listingstatus.status)}, status=status.HTTP_200_OK)
