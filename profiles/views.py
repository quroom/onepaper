# from pytz import timezone
from datetime import datetime

from allauth.account.views import SignupView
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Exists, Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.translation import ugettext as _
from rest_framework import generics, mixins, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from core.iamport import Iamport
from papers.models import Contractor, Paper, PaperStatus
from profiles.forms import CustomUserForm
from profiles.models import (
    AllowedUser,
    Certification,
    CustomUser,
    ExpertProfile,
    Insurance,
    Mandate,
    Profile,
    UserSetting,
)
from profiles.permissions import (
    IsAdmin,
    IsAuthorOrDesignator,
    IsOwner,
    IsOwnerOrReadonly,
    IsProfileUserOrReadonly,
)
from profiles.serializers import (
    ApproveExpertSerializer,
    CertificationSerializer,
    CustomUserIDNameSerializer,
    CustomUserSerializer,
    ExpertProfileReadonlySerializer,
    ExpertProfileSerializer,
    InsuranceSerializer,
    MandateEveryoneSerializer,
    MandateReadOnlySerializer,
    MandateSerializer,
    ProfileBasicInfoSerializer,
    ProfileReadonlySerializer,
    ProfileSerializer,
    UserSettingSerializer,
)


class AllowedProfileList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profiles = (
            Profile.objects.filter(allowed_user__allowed_users=request.user)
            .filter(is_activated=True)
            .select_related("user", "address", "expert_profile")
        )
        serializer = ProfileReadonlySerializer(profiles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AllowedUserDetail(APIView, PageNumberPagination):
    permission_classes = [IsAuthenticated, IsProfileUserOrReadonly]
    lookup_field = "pk"

    def get_object(self, pk):
        obj = get_object_or_404(AllowedUser, profile=pk)
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, pk):
        allowedUser = self.get_object(pk)
        allowed_users = allowedUser.allowed_users.exclude(id=request.user.id)
        page = self.paginate_queryset(allowed_users, request, view=self)
        serializer = CustomUserIDNameSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def post(self, request, pk):
        allowedUser = self.get_object(pk)

        if request.data["allowed_users"]["email"] == request.user.email:
            return Response(
                {"detail": ValidationError(_("자기 자신의 이메일은 추가할 수 없습니다."))},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            user = CustomUser.objects.get(email=request.data["allowed_users"]["email"])
        except CustomUser.DoesNotExist:
            return Response(
                {"detail": ValidationError(_("존재하지 않는 이메일 입니다."))},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if user in allowedUser.allowed_users.all():
            return Response(
                {"detail": ValidationError(_("이미 추가된 회원입니다."))}, status=status.HTTP_400_BAD_REQUEST
            )

        allowedUser.allowed_users.add(user)
        allowedUser.save()

        allowed_users = allowedUser.allowed_users.exclude(id=request.user.id)
        page = self.paginate_queryset(allowed_users, request, view=self)
        serializer = CustomUserIDNameSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def delete(self, request, pk):
        allowedUser = self.get_object(pk)

        if request.user.email in request.data["allowed_users"]:
            return Response(
                {"detail": ValidationError(_("자신의 이메일은 삭제할 수 없습니다."))},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user_list = allowedUser.allowed_users.filter(email__in=request.data["allowed_users"])

        if user_list.count() != len(request.data["allowed_users"]):
            return Response(
                {"detail": ValidationError(_("빠른거래 리스트에 추가되지 않은 회원은 삭제 할 수 없습니다."))},
                status=status.HTTP_400_BAD_REQUEST,
            )

        response = allowedUser.allowed_users.remove(*user_list)
        response = allowedUser.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class ApproveExpert(
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    queryset = ExpertProfile.objects.filter(profile__is_activated=True)
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = ApproveExpertSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        if len(request.data["profiles"]) == 0:
            return Response(
                {"detail": ValidationError(_("전문가가 선택되지 않았습니다."))},
                status=status.HTTP_400_BAD_REQUEST,
            )

        queryset = self.get_queryset()
        expert_profiles = queryset.filter(id__in=request.data["profiles"]).exclude(
            status=ExpertProfile.APPROVED
        )
        if expert_profiles.exists() is False:
            return Response(
                {"detail": ValidationError(_("승인 가능한 전문가가 선택되지 않았습니다."))},
                status=status.HTTP_400_BAD_REQUEST,
            )
        expert_profiles.update(status=ExpertProfile.APPROVED)

        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
        serializer = self.get_serializer(queryset, many=True)
        return self.get_paginated_response(serializer.data)

    def delete(self, request):
        expert_profiles = ExpertProfile.objects.filter(id__in=request.data["profiles"])
        if expert_profiles.exists() is False:
            return Response(
                {"detail": ValidationError(_("전문가가 선택되지 않았습니다."))},
                status=status.HTTP_400_BAD_REQUEST,
            )
        expert_profiles.update(status=ExpertProfile.DENIED)
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
        serializer = self.get_serializer(queryset, many=True)
        return self.get_paginated_response(serializer.data)


class CertificateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsOwner]

    def put(self, request):
        imp_uid = request.data.get("imp_uid")
        if imp_uid == None:
            return Response(
                {"detail": ValidationError(_("Certficiation is failed. imp_uid is none."))},
                status=status.HTTP_400_BAD_REQUEST,
            )
        iamport = Iamport()
        try:
            certificationsInfo = iamport.find_certification(imp_uid)
            certified_at = certificationsInfo.get("certified_at")
            di = certificationsInfo.get("unique_in_site")
            if di == None:
                return Response(
                    {"detail": ValidationError(_("Certification was not sucessful"))},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            else:
                try:
                    duplicate_di = Certification.objects.exclude(profile__user=request.user).get(
                        di=di
                    )
                    return Response(
                        {
                            "detail": ValidationError(
                                _(
                                    "There are other accounts that have already been authenticated. e-mail     : %(email)s"
                                )
                                % {"email": duplicate_di.profile.user.email}
                            )
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                except Certification.DoesNotExist:
                    profile = get_object_or_404(Profile, user=self.request.user, is_activated=True)
                    if (
                        certificationsInfo.get("name") == profile.user.name
                        and certificationsInfo.get("birthday") == str(profile.user.birthday)
                        and certificationsInfo.get("phone") == profile.mobile_number
                    ):
                        pass
                    else:
                        return Response(
                            {
                                "detail": ValidationError(
                                    _(
                                        "The name/birth/mobile phone number you entered does not match your profile information."
                                    )
                                )
                            },
                            status=status.HTTP_400_BAD_REQUEST,
                        )

        except Iamport.ResponseError as e:
            return Response({"detail": e.message}, status=e.code)
        except Iamport.HttpError as e:
            return Response({"detail": e.message}, status=e.code)

        certification = profile.certification
        certification.updated_at = timezone.make_aware(datetime.fromtimestamp(certified_at))
        certification.imp_uid = imp_uid
        certification.di = di
        certification.save()
        serializer = CertificationSerializer(certification)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ExpertProfileList(APIView):
    permission_classes = [IsAuthenticated, IsOwner]

    def get(self, request):
        queryset = Profile.objects.filter(
            user=self.request.user,
            expert_profile__status=ExpertProfile.APPROVED,
            is_activated=True,
        ).select_related("user", "address", "expert_profile")
        serializer = ProfileReadonlySerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class InsuranceViewset(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = InsuranceSerializer

    def get_queryset(self):
        return Insurance.objects.filter(
            expert_profile__profile__user=self.request.user,
            expert_profile__profile=self.kwargs["profile_pk"],
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if not self.request.method in SAFE_METHODS:
            context["profile_pk"] = self.kwargs["profile_pk"]
            context["pk"] = self.kwargs.get("pk")
        return context

    @transaction.atomic
    def perform_create(self, serializer):
        expert_profile = ExpertProfile.objects.get(profile__id=self.kwargs["profile_pk"])
        serializer.save(expert_profile=expert_profile)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        from_date = request.data.get("from_date")
        to_date = request.data.get("to_date")
        instance = self.get_object()

        if from_date == None or to_date == None:
            return Response(
                {"detail": ValidationError(_("보증서류 시작일과 종료일을 모두 입력해주세요."))},
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            from_date = datetime.strptime(from_date, "%Y-%m-%d")
            to_date = datetime.strptime(to_date, "%Y-%m-%d")
            if from_date.date() != instance.from_date or to_date.date() != instance.to_date:
                local_time = timezone.localtime()
                tzinfo = local_time.tzinfo
                from_date_time = datetime.combine(from_date, datetime.min.time(), tzinfo=tzinfo)
                to_date_time = datetime.combine(to_date, datetime.max.time(), tzinfo=tzinfo)
                instance_from_date_time = datetime.combine(
                    instance.from_date, datetime.min.time(), tzinfo=tzinfo
                )
                instance_to_date_time = datetime.combine(
                    instance.to_date, datetime.max.time(), tzinfo=tzinfo
                )
                related_papers = Paper.objects.filter(
                    verifying_explanation__insurance=instance,
                    updated_at__gte=instance_from_date_time,
                    updated_at__lte=instance_to_date_time,
                )
                if related_papers.exists() and from_date.date() != instance.from_date:
                    return Response(
                        {
                            "detail": ValidationError(
                                _("보증서류가 포함된 거래계약서가 있는 경우 보증서류 시작일을 변경할 수 없습니다.")
                            )
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                after_updated_related_papers = Paper.objects.filter(
                    verifying_explanation__insurance=instance,
                    updated_at__gte=from_date_time,
                    updated_at__lte=to_date_time,
                )

                # FIXME Need to add test code for this logic.
                if related_papers.count() != after_updated_related_papers.count():
                    return Response(
                        {
                            "detail": ValidationError(
                                _("수정 후 보증서류 기간에 제외되는 계약서가 없도록 기간을 다시 수정해주세요.")
                            )
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        local_time = timezone.localtime()
        tzinfo = local_time.tzinfo
        instance_from_date_time = datetime.combine(
            instance.from_date, datetime.min.time(), tzinfo=tzinfo
        )
        instance_to_date_time = datetime.combine(
            instance.to_date, datetime.max.time(), tzinfo=tzinfo
        )
        related_papers = Paper.objects.filter(
            verifying_explanation__insurance=instance,
            updated_at__gte=instance_from_date_time,
            updated_at__lte=instance_to_date_time,
        )

        if related_papers.exists():
            return Response(
                {"detail": ValidationError(_("보증서류가 포함된 거래계약서가 있는 경우 보증서류 정보를 삭제할 수 없습니다."))},
                status=status.HTTP_400_BAD_REQUEST,
            )
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProfileViewset(ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        if self.request.user.is_expert:
            return Profile.objects.filter(user=self.request.user).select_related("user", "address")
        else:
            return Profile.objects.filter(user=self.request.user).select_related(
                "user", "address", "expert_profile"
            )

    def get_serializer_class(self):
        if self.request.user.is_expert:
            if self.request.method in SAFE_METHODS:
                return ExpertProfileReadonlySerializer
            else:
                return ExpertProfileSerializer
        else:
            if self.request.method in SAFE_METHODS:
                return ProfileReadonlySerializer
            else:
                return ProfileSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", True)
        obj = self.get_object()
        expert_profile = getattr(obj, "expert_profile", None)
        if not expert_profile is None:
            if (
                expert_profile.status != ExpertProfile.REQUEST
                and expert_profile.status != ExpertProfile.DENIED
            ):
                return Response(
                    {"detail": ValidationError(_("승인된 전문가 프로필은 수정 할 수 없습니다. 새 프로필을 만드세요."))},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        if (
            Contractor.objects.filter(profile=obj)
            .exclude(paper__status__status=PaperStatus.REQUESTING)
            .exists()
        ):
            return Response(
                {"detail": ValidationError(_("요청단계 이후 계약서가 있는 경우 프로필을 수정할 수 없습니다."))},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if (
            Mandate.objects.filter(designator=obj).exists()
            or Mandate.objects.filter(designee=obj).exists()
        ):
            return Response(
                {"detail": ValidationError(_("작성한 위임장이 있는 경우 프로필을 수정할 수 없습니다."))},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if Certification.objects.filter(profile=obj).exclude(di="").exists():
            if request.data.get("mobile_number") != obj.mobile_number:
                return Response(
                    {"detail": ValidationError(_("본인인증 완료된 프로필의 휴대폰 번호는 수정할 수 없습니다."))},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        serializer = self.get_serializer(obj, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_update(serializer)
        instance_serializer = ExpertProfileReadonlySerializer(instance)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        return Response(instance_serializer.data)

    def perform_update(self, serializer):
        return serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        instance_serializer = ExpertProfileReadonlySerializer(instance)
        headers = self.get_success_headers(instance_serializer.data)
        return Response(instance_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @transaction.atomic
    def perform_create(self, serializer):
        Profile.objects.filter(user=self.request.user, is_activated=True).update(
            is_activated=False
        )
        return serializer.save(user=self.request.user, is_activated=True)

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if (
            Contractor.objects.filter(profile=instance)
            .exclude(paper__status__status=PaperStatus.REQUESTING)
            .exists()
        ):
            return Response(
                {"detail": ValidationError(_("요청단계 이후 계약서가 있는 경우 프로필을 삭제할 수 없습니다."))},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if (
            Mandate.objects.filter(designator=instance).exists()
            or Mandate.objects.filter(designee=instance).exists()
        ):
            return Response(
                {"detail": ValidationError(_("작성한 위임장이 있는 경우 프로필을 삭제할 수 없습니다."))},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if instance.is_activated and Profile.objects.filter(user=instance.user).exists():
            profile = Profile.objects.filter(user=instance.user).last()
            profile.is_activated = True
            profile.save()

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomUserViewset(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    permission_classes = [IsAuthenticated]
    model = CustomUser
    serializer_class = CustomUserSerializer

    def get_object(self):
        return self.request.user

    def list(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", True)
        instance = self.get_object()
        if (
            Paper.objects.filter(paper_contractors__profile__user=instance)
            .exclude(status__status=PaperStatus.REQUESTING)
            .exists()
        ):
            return Response(
                {"detail": ValidationError(_("요청단계 이후 계약서가 있는 경우 회원 정보를 수정할 수 없습니다."))},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if Certification.objects.filter(profile__user=instance).exclude(di="").exists():
            return Response(
                {"detail": ValidationError(_("본인인증 완료된 회원정보는 수정할 수 없습니다."))},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            if not (
                instance.email == request.data["email"] and instance.name == request.data["name"]
            ):
                return Response(
                    {"detail": ValidationError(_("입력하신 정보가 현재 회원의 정보와 일치하지 않습니다."))},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except KeyError:
            return Response(
                {"detail": ValidationError(_("탈퇴할 회원의 정보를 모두 입력해주세요."))},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if (
            Paper.objects.filter(paper_contractors__profile__user=instance)
            .exclude(status__status=PaperStatus.REQUESTING)
            .exists()
        ):
            instance.is_activated = False
            instance.save()
            return Response({"user_delete": _("탈퇴처리 되었습니다.")}, status=status.HTTP_200_OK)
        else:
            instance.delete()
            return Response(
                {"user_delete": _("탈퇴처리 되었습니다. 계정정보 또한 완전히 삭제되었습니다.")}, status=status.HTTP_200_OK
            )


class MandateViewset(ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsAuthorOrDesignator()]
        return super(MandateViewset, self).get_permissions()

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return MandateReadOnlySerializer
        else:
            return MandateSerializer

    def get_queryset(self):
        mandates = (
            Mandate.objects.all()
            .select_related(
                "address",
                "designator",
                "designator__address",
                "designator__user",
                "designee",
                "designee__address",
                "designee__user",
                "author",
            )
            .prefetch_related("designator__expert_profile", "designee__expert_profile")
        )
        return (
            mandates.filter(designator__user=self.request.user)
            | mandates.filter(designee__user=self.request.user)
        ).distinct()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = get_object_or_404(Mandate, pk=self.kwargs.get("pk"))
        if (
            instance.designator.user != self.request.user
            and instance.designee.user != self.request.user
        ):
            serializer = MandateEveryoneSerializer(instance)
        else:
            serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", True)
        instance = self.get_object()

        if bool(instance.designator_signature):
            return Response(
                {"detail": ValidationError(_("서명이 완료된 위임장은 수정할 수 없습니다."))},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if bool(instance.designator_signature):
            return Response(
                {"detail": ValidationError(_("서명이 완료된 위임장은 삭제할 수 없습니다."))},
                status=status.HTTP_400_BAD_REQUEST,
            )

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class OpenProfileList(APIView, PageNumberPagination):
    def get(self, request, format=None):
        email = self.request.query_params.get("email")
        mobile_number = self.request.query_params.get("mobile_number")

        if email and mobile_number:
            profiles = Profile.objects.filter(
                user__email=email, mobile_number=mobile_number, is_activated=True
            )
        elif email:
            profiles = Profile.objects.filter(user__email=email, is_activated=True)
        elif mobile_number:
            profiles = Profile.objects.filter(mobile_number=mobile_number, is_activated=True)
        else:
            return Response(
                {"detail": ValidationError(_("이메일 또는 연락처를 입력해야 합니다."))},
                status=status.HTTP_400_BAD_REQUEST,
            )

        profiles = profiles.exclude(user=request.user)
        page = self.paginate_queryset(profiles, request, view=self)
        serializer = ProfileBasicInfoSerializer(page, many=True, context={"request": request})
        return self.get_paginated_response(serializer.data)


class OpenProfileDetail(APIView):
    def get_object(self, pk):
        return get_object_or_404(Profile, pk=pk)

    def get(self, request, pk, format=None):
        profile = self.get_object(pk)
        serializer = ProfileBasicInfoSerializer(profile, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)


# FIXME Implment in frontend.
class ActivateProfile(APIView):
    permission_classes = [IsAuthenticated, IsOwner]

    def post(self, request, pk):
        profile = get_object_or_404(Profile, pk=pk)
        self.check_object_permissions(self.request, profile)
        active_profiles = Profile.objects.filter(user=self.request.user, is_activated=True)
        with transaction.atomic():
            active_profiles.update(is_activated=False)
            profile.is_activated = True
            profile.save()
        serializer = ProfileReadonlySerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserSettingAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user_setting = get_object_or_404(UserSetting, user=self.request.user)
        serializer = UserSettingSerializer(user_setting, request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
