from papers.models import Paper, Signature
from papers.serializers import PaperSerializer
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Signature)
def create_signature(sender, instance, created, **kwargs):
  paper = instance.paper
  seller = paper.seller
  buyer = paper.buyer
  expert = paper.expert
  expert_signed = True
  seller_signed = False
  buyer_signed = False

  if paper.status == Paper.DRAFT:
    if not expert is None :        
      expert_signed = paper.paper_signatures.filter(updated_at__gt=paper.updated_at, user=expert.user).exists()
    buyer_signed = paper.paper_signatures.filter(updated_at__gt=paper.updated_at, user=buyer.user).exists()
    seller_signed = paper.paper_signatures.filter(updated_at__gt=paper.updated_at, user=seller.user).exists()

    if(expert_signed and buyer_signed and seller_signed):
      paper.status = Paper.DONE
      paper.save()
  elif paper.status == Paper.DONE:
    is_seller_confirmed = paper.paper_signatures.filter(user=seller.user).last().is_confirmed
    is_buyer_confirmed = paper.paper_signatures.filter(user=buyer.user).last().is_confirmed
    is_expert_confirmed = True

    if not expert is None :
      expert_signature = paper.paper_signatures.filter(user=expert.user).last()
      is_expert_confirmed = expert_signature.is_confirmed
    
    if(is_expert_confirmed and is_seller_confirmed and is_buyer_confirmed):
      paper.status = Paper.CONFIRMED
      paper.save()