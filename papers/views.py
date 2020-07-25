from django.db.models import Q
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from papers.models import Paper
from papers.serializers import PaperSerializer
from papers.permissions import IsAuthor, IsAuthorOrParticiations

class PaperViewset(ModelViewSet):
    queryset = Paper.objects.all()
    permission_classes = [IsAuthenticated, IsAuthorOrParticiations]
    serializer_class = PaperSerializer

    def destroy(self, request, *args, **kwargs):
        # FIX: Make destory function works well.
        # instance = self.get_object()
        # if instance.seller_signature == None\
        #    and instance.buyer_signature == None:
        #         self.perform_destroy(instance)
        #         return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def list(self, request, *args, **kwargs):
        # queryset = Paper.objects.filter(expert__user=self.request.user)
        # FIX: Call list function by each user type like expert, seller, buyer filter.
        queryset = Paper.objects.filter(Q(author=self.request.user) | Q(expert__user=self.request.user) | Q(seller__user=self.request.user) | Q(buyer__user=self.request.user)).distinct()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def get_permissions(self):
        if self.action == 'update' or self.action == "partial_update" or self.action == "destroy":
            return [IsAuthenticated(), IsAuthor()]
        return super(PaperViewset, self).get_permissions()