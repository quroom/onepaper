from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse

from listings.models import AskListing, ListingVisit


@receiver(post_save, sender=ListingVisit)
def create_listingvisit(sender, instance, created, **kwargs):
    current_site = Site.objects.get_current()
    domain = current_site.domain
    email_body = """\
        <html>
        <head></head>
        <body>
            <a href="%s">%s</h2>
        </body>
        </html>
        """ % (
        "https://" + domain + "/asklistings",
        "입주문의 리스트 바로가기",
    )
    instance.listing.author.email_user("[원페이퍼] 새로운 입주문의", html_message=email_body)


@receiver(post_save, sender=AskListing)
def create_asklisting(sender, instance, created, **kwargs):
    current_site = Site.objects.get_current()
    domain = current_site.domain
    email_body = """\
        <html>
        <head></head>
        <body>
            <a href="%s">%s</h2>
        </body>
        </html>
        """ % (
        "https://" + domain + "/asklistings",
        "매물요청 리스트 바로가기",
    )
    send_mail("[원페이퍼] 새로운 매물요청", None, None, ["inspireworld@naver.com"], html_message=email_body)
