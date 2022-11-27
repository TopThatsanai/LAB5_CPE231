"""lab5 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from invoice import views
from receipt import views as receipt_views
from report import views as report_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('product/list', views.ProductList.as_view(), name='product_list'),
    path('customer/list', views.CustomerList.as_view(), name='customer_list'),
    path('customer/detail/<customer_code>', views.CustomerDetail.as_view(), name='customer_detail'),
    path('payment_method/detail/<payment_metod>',receipt_views.PaymentMethodDetail.as_view(), name='paymentmedthod_detail'),


    path('invoice/list', views.InvoiceList.as_view(), name='invoice_list'),
    path('invoice/detail/<str:pk>/<str:pk2>', views.InvoiceDetail.as_view(), name='invoice_detail'),
    path('invoice/create', views.InvoiceCreate.as_view(), name='invoice_create'),
    path('invoice/update', views.InvoiceUpdate.as_view(), name='invoice_update'),
    path('invoice/delete', views.InvoiceDelete.as_view(), name='invoice_delete'),
    path('invoice/report/<str:pk>/<str:pk2>', views.InvoiceReport.as_view(), name='invoice_report'),

    path('invoice',views.index, name='index'),

    path('receipt', receipt_views.index, name='index'),
    path('receipt/list', receipt_views.ReceiptList.as_view(), name='receipt_list'),
    path('receipt/detail/<str:pk>/<str:pk2>', receipt_views.ReceiptDetail.as_view(), name='receipt_detail'),
    path('receipt/create', receipt_views.ReceiptCreate.as_view(), name='receipt_create'),
    path('receipt/update/<str:pk>/<str:pk2>', receipt_views.ReceiptUpdate.as_view(), name='receipt_update'),
    path('receipt/delete/<str:pk>/<str:pk2>', receipt_views.ReceiptDelete.as_view(), name='receipt_delete'),
    path('receipt/report/<str:pk>/<str:pk2>', receipt_views.ReceiptReport.as_view(), name='receipt_report'),
    path('payment_method/list', receipt_views.PaymentMethodList.as_view(), name='paymentmethod_list'),
    path('receipt_line_item/list', receipt_views.Receipt_line_item_List.as_view(), name = 'receiptlineitem_list'),

    path('report', report_views.index, name='index'),
    path('report/ReportListAllInvoices', report_views.ReportListAllInvoices),
    path('report/ReportProductsSold', report_views.ReportProductsSold),
    path('report/ReportListAllProducts', report_views.ReportListAllProducts),
    path('report/ReportListAllReceipts', report_views.ReportListAllReceipt),
    path('report/ReportUnpaidInvoices', report_views.ReportUnpaidInvoices),
]
