import xadmin, csv
from .models import Category, Manufacturer, Item
from django.http import HttpResponse

def generate_report(modeladmin, request, queryset):
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'inline; filename="report.csv"'
	writer = csv.writer(response)
	writer.writerow(['Name', 'Category', 'Manufacturer', 'Size', 'Date Expiry', 'Unit Price', 'Quantity in Units', 'Status'])
	purchases = queryset.values_list("name", "category", "manufacturer", "size", "date_expiry", "price_per_unit", "quantity_in_units", "status")
	for purchase in purchases:
		writer.writerow(purchase)
	return response
generate_report.short_description = 'Generate Report for Selected Items'

class ItemAdmin(object):
	date_hierarchy = 'date_expiry'
	list_display = ("name", "category", "manufacturer", "size", "date_expiry", "price_per_unit", "quantity_in_units", "status")
	list_display_links = ("name",)
	search_fields = ["name", "category__name", "manufacturer__name"]
	list_export = ('xls', 'xml', 'json')
	list_editable = ['status', 'date_expiry']
	#refresh_times = (3, 5)
	list_filter = ["name", "category", "manufacturer", "size", "date_expiry", "quantity_in_units", "status"]
	actions = [generate_report]
	show_bookmarks = False

xadmin.site.register(Category)
xadmin.site.register(Manufacturer)
xadmin.site.register(Item, ItemAdmin)
