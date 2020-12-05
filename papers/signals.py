from papers.models import Paper, ExplanationSignature, Signature, Contractor, PaperStatus
from profiles.models import Mandate
from papers.serializers import PaperSerializer
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

@receiver(post_save, sender=Signature)
@receiver(post_save, sender=ExplanationSignature)
def create_signature(sender, instance, created, **kwargs):
    if created == False:
        paper = instance.contractor.paper
        contractors = paper.paper_contractors.all()
        expert_exists = contractors.filter(group=Contractor.EXPERT).exists()
        mandates = Mandate.objects.filter(address__old_address=paper.address.old_address, designee__user=paper.author, designator_id__in=contractors.values("profile"))
        if mandates.exists():
            contractors = contractors.exclude(profile__in=mandates.values("designator"))
        signatures = Signature.objects.filter(
            updated_at__gte=paper.updated_at, contractor__in=contractors)
        explanation_signatures = ExplanationSignature.objects.filter(
            updated_at__gte=paper.updated_at, contractor__in=contractors)
        if paper.status.status == PaperStatus.DRAFT:
            if signatures.count() > 0 or explanation_signatures.count() > 0:
                status_instance = paper.status
                status_instance.status = PaperStatus.PROGRESS
                status_instance.save()
        elif signatures.count() == contractors.count():
            if expert_exists == True:
                if explanation_signatures.count() == contractors.count():
                    status_instance = paper.status
                    status_instance.status = PaperStatus.DONE
                    status_instance.save()
            else:
                status_instance = paper.status
                status_instance.status = PaperStatus.DONE
                status_instance.save()

@receiver(post_save, sender=Paper) 
def save_paper(sender, instance, created, **kwargs):
    status_instance = instance.status
    if status_instance.status != PaperStatus.DRAFT:
        status_instance.status = PaperStatus.DRAFT
        status_instance.save()

@receiver(post_delete, sender=Paper)
def delete_relataive_data(sender, instance, **kwargs):
    if not instance.status is None:
        instance.status.delete()
    if not instance.address is None:
        instance.address.delete()