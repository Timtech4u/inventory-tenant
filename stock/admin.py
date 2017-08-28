import csv
from django.contrib import admin
from .models import Category, Manufacturer, Item, Section
from django.http import HttpResponse
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from grappelli_filters import RelatedAutocompleteFilter, FiltersMixin
from grappelli_filters import SearchFilter

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

class ItemResource(resources.ModelResource):
    class Meta:
        model = Item
        fields = ("name", "category", "manufacturer", "size", "date_expiry", "price_per_unit", "quantity_in_units", "status",)
        export_order = ("name", "category", "manufacturer", "size", "date_expiry", "price_per_unit", "quantity_in_units", "status")
        skip_unchanged = True
        report_skipped = True

class ItemResourceAdmin(ImportExportModelAdmin, admin.ModelAdmin):
	resource_class = ItemResource
	date_hierarchy = 'date_expiry'
	list_display = ("name", "category", "manufacturer", "size", "price_per_unit", "quantity_in_units", "status")
	list_display_links = ("name",)
	search_fields = ["name", "category__name", "manufacturer__name"]
	list_export = ('xls', 'xml', 'json')
	list_editable = ['status', "price_per_unit", "quantity_in_units",]
	#refresh_times = (3, 5)
	list_filter = ["category", "manufacturer", "section", "date_expiry", "status",]
	actions = [generate_report]

class ItemProxy(Item):
	class Meta:
		proxy = True
		verbose_name = "Items"
		verbose_name_plural = "Items"

#admin.site.register(Item, ItemAdmin)
admin.site.register(ItemProxy, ItemResourceAdmin)
admin.site.register(Section)
admin.site.register(Category)
admin.site.register(Manufacturer)