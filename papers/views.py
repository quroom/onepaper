from django.core.exceptions import ValidationError
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from papers.models import Paper, Signature
from papers.serializers import PaperSerializer, SignatureSerializer
from papers.permissions import IsAuthor, IsAuthorOrParticiations, IsParticiations, IsProfileUser


class HidePaperApiView(APIView):
    def post(self, request, pk):
        paper = get_object_or_404(Paper, pk=pk)
        if paper.status == Paper.DONE:
            signatures = Signature.objects.filter(paper=paper)
            signature = signatures.get(
                profile__user=self.request.user) if signatures.exists() else None
            if signature is None:
                raise ValidationError("서명이 되지 않은 계약서는 숨길 수 없습니다.")
            else:
                signature.is_paper_visible = not signature.is_paper_visible
                signature.save()
        else:
            raise ValidationError("완료되지 않은 계약서는 숨길 수 없으며, 삭제만 가능합니다.")


class PaperViewset(ModelViewSet):
    queryset = Paper.objects.all()
    permission_classes = [IsAuthenticated, IsAuthorOrParticiations]
    serializer_class = PaperSerializer

    def destroy(self, request, *args, **kwargs):
        # FIX: Make destory function works well.
        instance = self.get_object()
        if not instance.status == Paper.DONE and not instance.status == Paper.HIDDEN:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        raise ValidationError("서명이 완료되어 계약서를 삭제할 수 없습니다.")

    def list(self, request, *args, **kwargs):
        # queryset = Paper.objects.filter(expert__user=self.request.user)
        # FIX: Call list function by each user type like expert, seller, buyer filter.
        queryset = Paper.objects.filter(Q(author=self.request.user) | Q(expert__user=self.request.user) | Q(
            seller__user=self.request.user) | Q(buyer__user=self.request.user)).distinct()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def get_permissions(self):
        if self.action in ['update', "partial_update", "destroy"]:
            return [IsAuthenticated(), IsAuthor()]
        return super(PaperViewset, self).get_permissions()


class SignatureListApiView(generics.ListAPIView):
    serializer_class = SignatureSerializer
    permission_classes = [IsAuthenticated, IsProfileUser]

    def get_queryset(self):
        kwarg_id = self.kwargs.get("id")
        return Signature.objects.filter(paper=kwarg_id)


class SignatureCreateApiView(generics.CreateAPIView):
    queryset = Signature.objects.all()
    serializer_class = SignatureSerializer
    permission_classes = [IsAuthenticated, IsParticiations]

    def perform_create(self, serializer):
        save_flag = False
        is_signature_done_dic = {
            'expert': False,
            'seller': False,
            'buyer': False,
        }
        request_user = self.request.user
        id = self.kwargs.get("id")
        paper = get_object_or_404(Paper, id=id)
        expert = getattr(paper.expert, 'user', None)
        seller = getattr(paper.seller, 'user', None)
        buyer = getattr(paper.buyer, 'user', None)

        if paper.status == Paper.DONE:
            raise ValidationError("계약서 작성이 완료되어 서명을 추가할 수 없습니다.")

        signatures = Signature.filter(paper=paper)
        if expert == request_user:
            if signatures.filter(profile=expert).exists():
                raise ValidationError("이미 서명이 등록되어있습니다.")
            else:
                serializer.save(paper=paper, profile=paper.expert)
                save_flag = True
        if seller == request_user:
            if signatures.filter(profile=seller).exists():
                raise ValidationError("이미 서명이 등록되어있습니다.")
            else:
                serializer.save(paper=paper, profile=paper.seller)
                save_flag = True
        if buyer == request_user:
            if signatures.filter(profile=buyer).exists():
                raise ValidationError("이미 서명이 등록되어있습니다.")
            else:
                serializer.save(paper=paper, profile=paper.buyer)
                save_flag = True
        if not save_flag:
            raise ValidationError(
                "계약서에 서명을 추가할 권한이 없습니다. 계약서 작성자에게 프로필 추가를 요청하세요.")

        if expert is not None:
            if Signature.objects.filter(paper=paper, profile=paper.expert).exists():
                is_signature_done_dic['expert'] = True
        else:
            is_signature_done_dic['expert'] = True

        if seller is not None:
            if Signature.objects.filter(paper=paper, profile=paper.seller).exists():
                is_signature_done_dic['seller'] = True
        else:
            is_signature_done_dic['seller'] = True

        if buyer is not None:
            if Signature.objects.filter(paper=paper, profile=paper.buyer).exists():
                is_signature_done_dic['buyer'] = True
        else:
            is_signature_done_dic['buyer'] = True

        done_flag = all(
            flag == True for flag in is_signature_done_dic.values())

        if done_flag:
            paper.status = Paper.DONE
            paper.save()

        return Response(serializer.data)
