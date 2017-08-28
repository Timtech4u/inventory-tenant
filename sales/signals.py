from django.db.models.signals import post_save
from django.dispatch import receiver
from stock.models import Item
import datetime

@receiver(post_save, sender=Item)
def my_handler(sender, instance, created, **kwargs):
	pass

#post_save.connect(my_handler, sender=Item)