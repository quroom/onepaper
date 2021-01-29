from django.shortcuts import render
from rest_framework.viewsets import GenericViewSet, mixins
from rest_framework.permissions import IsAuthenticated
from helps.models import Notice
from helps.serializers import NoticeSeiralizer, NoticeListSerializer

class NoticeGenericVieset(mixins.ListModelMixin,
                          mixins.RetrieveModelMixin,
                          GenericViewSet):
    queryset = Notice.objects.select_related('author').all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'list':
            return NoticeListSerializer
        if self.action == 'retrieve':
            return NoticeSeiralizer