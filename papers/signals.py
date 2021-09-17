import datetime

from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from papers.models import (
    Contractor,
    ExplanationSignature,
    Paper,
    PaperStatus,
    Signature,
    VerifyingExplanation,
)
from papers.serializers import PaperSerializer
from profiles.models import Mandate


@receiver(post_save, sender=Signature)
@receiver(post_save, sender=ExplanationSignature)
def create_signature(sender, instance, created, **kwargs):
    paper = instance.contractor.paper
    contractors = paper.paper_contractors.prefetch_related(
        "signature", "explanation_signature"
    ).all()
    verifying_explanation = VerifyingExplanation.objects.filter(paper=paper)
    mandates = Mandate.objects.filter(
        address__old_address=paper.address.old_address,
        designee__user=paper.author,
        designator_id__in=contractors.values("profile"),
    ).exclude(designator_signature="", to_date__lt=datetime.datetime.now())
    if mandates.exists():
        contractors = contractors.exclude(profile__in=mandates.values("designator"))
    signatures_count = contractors.filter(signature__updated_at__gte=paper.updated_at).count()
    explanation_signatures_count = contractors.filter(
        explanation_signature__updated_at__gte=paper.updated_at
    ).count()
    if paper.status.status == PaperStatus.DRAFT:
        if signatures_count > 0 or explanation_signatures_count > 0:
            status_instance = paper.status
            status_instance.status = PaperStatus.PROGRESS
            status_instance.save()
    elif signatures_count == contractors.count():
        if verifying_explanation.exists() == True:
            if explanation_signatures_count == contractors.count():
                status_instance = paper.status
                status_instance.status = PaperStatus.DONE
                status_instance.save()
        else:
            status_instance = paper.status
            status_instance.status = PaperStatus.DONE
            status_instance.save()


@receiver(post_delete, sender=Paper)
def delete_relataive_data(sender, instance, **kwargs):
    if not instance.status is None:
        instance.status.delete()
    if not instance.address is None:
        instance.address.delete()


@receiver(post_save, sender=Contractor)
def save_contractor(sender, instance, created, **kwargs):
    if not created:
        status_instance = instance.paper.status
        if instance.paper.paper_contractors.filter(is_allowed=False).exists():
            status_instance.status = PaperStatus.DENIED
            status_instance.save()
        elif not instance.paper.paper_contractors.exclude(is_allowed=True).exists():
            if status_instance.status in (PaperStatus.REQUESTING, PaperStatus.DENIED):
                status_instance.status = PaperStatus.DRAFT
                status_instance.save()
        else:
            status_instance.status = PaperStatus.REQUESTING
            status_instance.save()


@receiver(post_save, sender=Paper)
def save_paper(sender, instance, created, **kwargs):
    status_instance = instance.status
    if (
        status_instance.status != PaperStatus.DRAFT
        and status_instance.status != PaperStatus.REQUESTING
    ):
        status_instance.status = PaperStatus.DRAFT
        status_instance.save()
