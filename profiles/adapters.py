from datetime import datetime

from allauth.account.adapter import DefaultAccountAdapter, app_settings, get_current_site
from allauth.account.utils import user_email, user_field, user_username
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class CustomAccountAdapter(DefaultAccountAdapter):
    def send_confirmation_mail(self, request, emailconfirmation, signup):
        current_site = get_current_site(request)
        activate_url = self.get_email_confirmation_url(request, emailconfirmation)
        ctx = {
            "user": emailconfirmation.email_address.user,
            "activate_url": activate_url,
            "current_site": current_site,
            "key": emailconfirmation.key,
            "expiration_days": app_settings.EMAIL_CONFIRMATION_EXPIRE_DAYS,
        }
        if signup:
            email_template = "account/email/email_confirmation_signup"
        else:
            email_template = "account/email/email_confirmation"
        self.send_mail(email_template, emailconfirmation.email_address.email, ctx)


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def get_signup_form_initial_data(self, sociallogin):
        social_account = sociallogin.account
        extra_data = social_account.extra_data
        if "name" in extra_data:
            self.fields["name"].initial = extra_data["name"]
        if social_account.provider == "naver":
            if "birthday" in extra_data and "birthyear" in extra_data:
                birthday = datetime(
                    int(extra_data["birthyear"]),
                    int(extra_data["birthday"].split("-")[0]),
                    int(extra_data["birthday"].split("-")[1]),
                )
        if social_account.provider == "kakao":
            kakao_account = extra_data.get("kakao_account")
            if kakao_account:
                name = kakao_account.get("profile").get("nickname")
                birthday = datetime(
                    int(kakao_account.get("birthyear")),
                    int(kakao_account.get("birthday")[0:2]),
                    int(kakao_account.get("birthday")[2:4]),
                )
        user = sociallogin.user
        initial = {
            "email": user_email(user) or "",
            "username": user_username(user) or "",
            "name": name,
            "birthday": birthday,
        }
        return initial
