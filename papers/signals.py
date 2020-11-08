from papers.models import Paper, Signature, Contractor
from papers.serializers import PaperSerializer
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Signature)
def create_signature(sender, instance, created, **kwargs):
    paper = instance.contractor.paper
    contractors = paper.paper_contractors.all()
    signatures = Signature.objects.filter(
        updated_at__gt=paper.updated_at, contractor__in=contractors)
    if paper.status == Paper.DRAFT:
        if signatures.count() == contractors.count():
            paper.status = Paper.DONE
            paper.save()
    elif paper.status == Paper.DONE:
        if signatures.filter(is_confiremd=True).count() == contractors.count():
            paper.status = Paper.CONFIRMED
            paper.save()
