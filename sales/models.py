from django.db import models
from stock.models import Item

class Purchase(models.Model):
    """
    Description: Model Description
    This Model serves for our daily purchases by Customer
    We'll be generating reports from this
    """
    date_sold = models.DateTimeField(auto_now_add=True)
    total_amount_to_be_paid_by_purchaser = models.IntegerField(help_text="This can be left as default, it will be automatically calculated", default=0)
    comments = models.CharField(max_length=200, blank=True, null=True, help_text='Extra Comments made by Purchaser')
    is_debtor = models.NullBooleanField(blank=True, null=True, help_text="Select if Customer Owes Cash")

    def __str__(self):
        return "Date: {} | Time: {} ".format(self.date_sold.strftime("%Y-%m-%d"),
                                                self.date_sold.strftime("%H:%M:%S"))
    
    class Meta:
        verbose_name = "Purchaser"
        verbose_name_plural = "Purchaser"
        ordering = ['-date_sold']



class PurchaseItem(models.Model):
    item = models.ForeignKey(Item, help_text='Type to Search or Select/Create an Item from Stock', )
    #available = AvailableManager()
    purchaser = models.ForeignKey(Purchase, help_text='Type to Search or Select/Create a Purchaser', on_delete=models.CASCADE)
    quantity_purchased = models.IntegerField(default=1, help_text='Enter Quantity of Item Purchased')
    price = models.IntegerField()

    @staticmethod
    def autocomplete_search_fields():
        return ("item__icontains",)

    class Meta:
        verbose_name = "Items Purchased"
        verbose_name_plural = "Items Purchased"
        ordering = ['-purchaser']

    @property
    def price(self):
        return self.quantity_purchased * self.item.price_per_unit

    def __str__(self):
        return "Purchased: {} of {} at N{}".format(self.quantity_purchased, 
                                                self.item.name,
                                                self.price)