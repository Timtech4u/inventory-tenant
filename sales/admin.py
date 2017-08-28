from django.contrib import admin
from .models import Purchase, PurchaseItem
#Imports for Generating Files
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
import csv

from admin_steroids.filters import AjaxFieldFilter

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

class PurchaseItemInline(admin.TabularInline):
    model = PurchaseItem
    extra = 1

class PurchaseAdmin(admin.ModelAdmin):
	date_hierarchy = 'date_sold'
	list_display = ("date_sold", "total_amount_to_be_paid_by_purchaser", "comments")
	list_display_links = ("date_sold",)
	search_fields = ["total_amount_to_be_paid_by_purchaser"]
	list_export = ('xls', 'xml', 'json')
	list_editable = ['total_amount_to_be_paid_by_purchaser']
	list_filter = ['date_sold', 'is_debtor']
	actions = [generate_report, print_receipt]
	inlines = [PurchaseItemInline]
	autocomplete_lookup_fields = {
   'fk': ['item'],
   }
	fieldsets = [
        ('Purchases Total',               {'fields': ['total_amount_to_be_paid_by_purchaser']}),
        ('Additional Information', {'fields': ['comments', 'is_debtor'], 'classes': ['collapse']}),
    ]

admin.site.register(Purchase, PurchaseAdmin)