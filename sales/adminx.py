#XAdmin Imports
import xadmin
from xadmin import views
from xadmin.plugins.inline import InlineModelAdmin
from django.contrib import admin
#Model Imports
from .models import PurchaseItem, Purchase
from stock.models import Item, Category, Manufacturer

#Imports for Generating Files
from django.http import HttpResponseRedirect, HttpResponse
import csv

from django.core.urlresolvers import reverse
from nested_admin import NestedModelAdmin, NestedStackedInline, NestedTabularInline
from stock.models import Item, ItemI18n

def generate_report(modeladmin, request, queryset):
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'inline; filename="report.csv"'
	writer = csv.writer(response)
	writer.writerow(['Date/Time', 'Item Purchased', 'Quantity', 'Total Amount Paid'])
	purchases = queryset.values_list('date_sold', 'purchaseitem__item__name', 'purchaseitem__quantity_purchased', 'total_amount_to_be_paid_by_purchaser')
	for purchase in purchases:
		writer.writerow(purchase)
	return response
generate_report.short_description = 'Generate Report for Selected Purchases'

def print_receipt(modeladmin, request, queryset):
    for obj in queryset:
    		#Returns User to print URL for Printing
           return HttpResponseRedirect(reverse('print', args=[obj.id]),)
print_receipt.short_description = 'Print Receipt for a Purchase'

#Adding Purchase Items as Inline 
class PurchaseItemInline(InlineModelAdmin):
    model = PurchaseItem
    extra = 1

class ItemI18nTabularInline(NestedTabularInline):
   model = ItemI18n
   extra = 1


class ItemStackedInline(NestedStackedInline):
   model = Item
   extra = 1
   inlines = [ItemI18nTabularInline, ]

class PurchaseItemInline(admin.TabularInline):
    model = PurchaseItem
    extra = 1

class PurchaseAdmin(object):
	list_display = ("date_sold", "total_amount_to_be_paid_by_purchaser")
	list_display_links = ("date_sold",)
	search_fields = ["total_amount_to_be_paid_by_purchaser"]
	list_export = ('xls', 'xml', 'json')
	list_editable = ['total_amount_to_be_paid_by_purchaser']
	#refresh_times = (3, 5)
	list_filter = ["total_amount_to_be_paid_by_purchaser"]
	actions = [generate_report, print_receipt]
	show_bookmarks = False
	inline = [PurchaseItemInline]

class PurchaseItemAdmin(object):
	list_display = ("purchaser", "item", "quantity_purchased", "price")
	list_display_links = ("purchaser",)
	list_export = ('xls', 'xml', 'json')
	list_editable = ['purchaser',]
	#refresh_times = (3, 5)
	list_filter = ["item"]
	show_bookmarks = False



xadmin.site.register(Purchase, PurchaseAdmin)
xadmin.site.register(PurchaseItem, PurchaseItemAdmin)

@xadmin.sites.register(views.CommAdminView)
class GlobalSetting(object):
    global_search_models = []
    global_models_icon = {
        PurchaseItem: "fa fa-laptop", Purchase: "fa fa-laptop", 
        Item: "fa fa-laptop", Category: "fa fa-laptop", Manufacturer: "fa fa-laptop"
    }
    menu_style = 'default'  # 'accordion'