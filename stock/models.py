from django.db import models
import uuid

STATUS_CHOICES = (
    ('a', 'Available'),
    ('u', 'Unavailable'),
    ('e', 'Expired'),
)

class Category(models.Model):
    name = models.CharField(max_length=50, help_text='Enter Category Name')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

class Manufacturer(models.Model):
    name = models.CharField(max_length=100, help_text='Enter Manufacturer Name')
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Manufacturers"
        ordering = ['name']

class Section(models.Model):
    name = models.CharField(max_length=100, help_text='Enter Section Name')
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Section"
        ordering = ['name']

class Item(models.Model):
    code = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, help_text='Enter Item Name')
    category = models.ForeignKey(Category, help_text='Select/Create Item Category')
    manufacturer = models.ForeignKey(Manufacturer, help_text='Select/Create Item Manufacturer')
    section = models.ForeignKey(Section, help_text='Select/Create Item Drug Section', blank=True, null=True)
    size = models.CharField(max_length=100, null=True, blank=True, help_text='Enter Item Size')
    date_added = models.DateField(auto_now_add=True)
    date_expiry = models.DateField(help_text='Enter Expiry Date of Item')
    quantity_in_units = models.IntegerField(help_text='Enter Item\'s Quantities in Units')
    price_per_unit = models.IntegerField(help_text='Enter Price for each Item\'s Unit')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='a', 
    							help_text='Select Item\'s Status')

    @staticmethod
    def autocomplete_search_fields():
        return 'category', 'manufacturer', 'section'

    class Meta:
        ordering = ['status']

    @property
    def description(self):
        #if self.status == 'a':
        return "Name: {} | Cat.: {} | Man.: {} | Size: {} ".format(self.name,
                                                                            self.category.name,
                                                                            self.manufacturer.name,
                                                                            self.size)
        """
        This should be done on the Notification App
        """
        # elif self.status == 'e':
        #     return "EXPIRED! - Name: {} - Category: {} - Manufacturer: {} - Size: {} ".format(self.name,
        #                                                                                         self.category.name,
        #                                                                                         self.manufacturer.name,
        #                                                                                         self.size)
        # elif self.status == 'u':
        #     return "UNAVAILABLE! - Name: {} - Category: {} - Manufacturer: {} - Size: {} ".format(self.name,
        #                                                                                       self.category.name,
        #                                                                                      self.manufacturer.name,
        #                                                                                      self.size)
    def __str__(self):
        return self.description

class ItemI18n(models.Model):
    name = models.CharField('Name i18n', max_length=164)
    item = models.ForeignKey(Item)

    class Meta:
        verbose_name = 'Item i18n'
        verbose_name_plural = 'Items i18n'