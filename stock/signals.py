from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from sales.models import PurchaseItem, Purchase
from stock.models import Item
import datetime

@receiver(post_save, sender=PurchaseItem)
def affect_item(sender, instance, created, **kwargs):
    #Check if the Model Is Created in Purchase Item
    if created:
        #Get related instances for Item and Purchaser
        item_bought = Item.objects.get(id=instance.item.id)
        purchaser = Purchase.objects.get(id=instance.purchaser.id)
        #Reduce Item Quantity in Stock
        item_bought.quantity_in_units -= instance.quantity_purchased
        #Adds Purchase Item Pricem to Purchaser's Total Amount
        purchaser.total_amount_to_be_paid_by_purchaser += instance.price
        #Checks if total amount is to be given discount
        if purchaser.total_amount_to_be_paid_by_purchaser >= 10000:
            purchaser.total_amount_to_be_paid_by_purchaser -= purchaser.total_amount_to_be_paid_by_purchaser * 0.05
            purchaser.comments += " NOTE: 5% Discount has been applied"
        #Resets Item in Stock to Available
        item_bought.status = 'a'
        #Checks if Item in Stock is Unavailable and Changes it.
        if item_bought.date_expiry <= datetime.date.today() + datetime.timedelta(days=1):
            item_bought.status = 'e'
        #Checks If Item is Unavailable
        if item_bought.quantity_in_units <= 1:
            item_bought.status = 'u'
        purchaser.save()
        item_bought.save()
    """
    TODO: 
        Extend this for updated fields e.g. When a Purchase Item is deleted
        Changes should be reflected in the Purchase Or A Message should be Passed to the Staff.
        Also Auto check for unavailable or expired items. 
    """