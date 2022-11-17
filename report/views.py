from django.shortcuts import render
from django.http import HttpResponse

from django.views.generic import View
from django.db import connection
from report.models import *

from django.db import connection

from django.http import JsonResponse

def index(request):
    #invoice_no = request.GET.get('inv','')
    #dataReport = dict()
    #dataReport['invoice'] = list(Invoice.objects.filter(invoice_no=invoice_no).values())
    #dataReport['invoice_line_item'] = list(InvoiceLineItem.objects.filter(invoice_no=invoice_no).values())
    #return JsonResponse(dataReport)
    return render(request, 'base_report.html')
#list(Invoice.objects.filter(invoice_no=invoice_no).select_related('customer_code').values('customer_code__name’))
#'invoice_no', 'date', 'customer_code_id', 'customer_code__name','due_date','total','vat','amount_due'

def ReportListAllProducts(request):

    dataReport = dict()
    data = list(Product.objects.all().values())
    columns = ("Code", "Name", "Units", "Product Type")
    dataReport['column_name'] = columns
    dataReport['data'] = data

    return render(request, 'report_list_all_products.html', dataReport)

def ReportListAllInvoices(request):
    cursor = connection.cursor()
    cursor.execute ('SELECT i.invoice_no as "Invoice No", i.date as "Date" '
                             ' , i.customer_code as "Customer Code", c.name as "Customer Name" '
                             ' , i.due_date as "Due Date", i.total as "Total", i.vat as "VAT", i.amount_due as "Amount Due" '
                             ' , ili.product_code as "Product Code", p.name as "Product Name" '
                             ' , ili.quantity as "Quantity", ili.unit_price as "Unit Price", ili.product_total as "Extended Price" '
                             ' FROM invoice i JOIN customer c ON i.customer_code = c.customer_code '
                             '  JOIN invoice_line_item ili ON i.invoice_no = ili.invoice_no '
                             '  JOIN product p ON ili.product_code = p.code '
                             ' ')
    dataReport = dict()
    columns = [col[0] for col in cursor.description]
    data = cursor.fetchall()
    dataReport['column_name'] = columns
    dataReport['data'] = CursorToDict(data,columns)

    return render(request, 'report_list_all_invoices.html', dataReport)

def ReportListAllPaymentmethod(request):
    
    dataReport = dict()
    data = list(Payment_method.objects.all().values())
    columns = ("payment_method", "description")
    dataReport['column_name'] = columns
    dataReport['data'] = data

    return render(request, 'report_Payment_method.html', dataReport)

def ReportListAllReceipt(request):
    cursor = connection.cursor()
    cursor.execute ('SELECT ' 
    'r.receipt_no as "Receipt No" , '
    'r.created_at as "Create At", r.customer_code as "Customer Code",' 
    'c.name as "Customer Name", pm.description as "Payment Method",' 
    'r.payment_reference as "Payment Reference",' 
    'r.total_recieved as "Total Received", '
    'r.remarks as "Remarks",' 
    'i.invoice_no as "Invoice No",' 
    'i.date as "Date",' 
    'i.amount_due as "Invoice Full Amount",' 
    'rli.amount_paid_here as "Amount Paid Here"'
    'FROM receipt as r '
    'JOIN receipt_line_item as rli ON r.receipt_no = rli.receipt_no ' 
    'JOIN invoice as i ON rli.invoice_no = i.invoice_no '
    'JOIN payment_method as pm ON r.payment_method = pm.payment_method ' 
    'JOIN customer c ON r.customer_code = c.customer_code')
    dataReport = dict()
    columns = [col[0] for col in cursor.description]
    data = cursor.fetchall()
    dataReport['column_name'] = columns
    dataReport['data'] = CursorToDict(data,columns)

    return render(request, 'report_list_all_Receipt.html', dataReport)

def ReportUnpaidInvoices(request):
    cursor1 = connection.cursor()
    cursor1.execute (  ' SELECT i.invoice_no as "Invoice Number", i.date as "Invoice Date", c.name as "Customer Name"'
                                ', i.amount_due as "Amount Due", rli.amount_paid_here as "Amount Received"'
                                ', i.amount_due - rli.amount_paid_here as "Amount Unpaid" '
                               'FROM receipt_line_item as rli JOIN invoice as i ON rli.invoice_no = i.invoice_no '
                               'JOIN customer as c ON c.customer_code = i.customer_code')

    columns1 = [col[0] for col in cursor1.description]
    data1 = cursor1.fetchall()

    cursor2 = connection.cursor()
    cursor2.execute ('SELECT count(i.invoice_no) as "Footer", SUM(i.amount_due - rli.amount_paid_here) as "Total Invoice Amount Not Paid"'
                              ', SUM(rli.amount_paid_here) as "Total Invoive Amount Received"'
                              'FROM receipt_line_item as rli JOIN invoice as i ON rli.invoice_no = i.invoice_no ')

    columns2 = [col[0] for col in cursor2.description]
    data2 = cursor2.fetchall()

    dataReport = dict()
    dataReport['column_name1'] = columns1
    dataReport['data1'] = CursorToDict(data1,columns1)

    dataReport['column_name2'] = columns2
    dataReport['data2'] = CursorToDict(data2,columns2)
    return render(request, 'report_Unpaid_Invoices.html', dataReport)


def ReportProductsSold(request):

    cursor = connection.cursor()
    cursor.execute ('SELECT ili.product_code as "Product Code", p.name as "Product Name" '
                    ' , SUM(ili.quantity) as "Total Quantity Sold", SUM(ili.product_total) as "Total Value Sold" '
                    ' FROM invoice i JOIN invoice_line_item ili ON i.invoice_no = ili.invoice_no '
                    '   JOIN product p ON ili.product_code = p.code '
                    ' GROUP BY p.code, ili.product_code, p.name '
                    ' ')
    dataReport = dict()
    columns = [col[0] for col in cursor.description]
    data = cursor.fetchall()
    dataReport['column_name'] = columns
    dataReport['data'] = CursorToDict(data,columns)

    return render(request, 'report_products_sold.html', dataReport)

def CursorToDict(data,columns):
    result = []
    fieldnames = [name.replace(" ", "_").lower() for name in columns]
    for row in data:
        rowset = []
        for field in zip(fieldnames, row):
            rowset.append(field)
        result.append(dict(rowset))
    return result