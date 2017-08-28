from django.shortcuts import render

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from sales.models import Purchase
from weasyprint import HTML, CSS

def print_receipt(request, purchase_id):
    purchaser = get_object_or_404(Purchase, id=purchase_id)
    purchaser_items =purchaser.purchaseitem_set.all()
    html_string = render_to_string('receipt.html', {'p': purchaser, 'pi': purchaser_items})
    html = HTML(string=html_string)
    html.write_pdf(target='/tmp/receipt.pdf');

    fs = FileSystemStorage('/tmp')
    with fs.open('receipt.pdf') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="receipt"'
        return response

    return response

def test_receipt(request):
    purchaser = Purchase.objects.get(id=9)
    purchaser_items =purchaser.purchaseitem_set.all()
    return render(request, 'receipt.html', {'p': purchaser, 'pi': purchaser_items})
