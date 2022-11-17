from pydoc import describe
from django.db import models

# Create your models here.
class Data(models.Model):
    key = models.CharField(max_length=10,primary_key=True)
    value= models.CharField(max_length=100)

class ProductType(models.Model):
    product_type = models.CharField(max_length=10,primary_key=True)
    description = models.CharField(max_length=100)
    class Meta:
        db_table = "product_type"
        managed = False
    def __str__(self):
        return self.product_type

class Product(models.Model):
    code = models.CharField(max_length=10,primary_key=True)
    name = models.CharField(max_length=100)
    units = models.CharField(max_length=10)
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE, db_column='product_type')
    class Meta:
        db_table = "product"
        managed = False
    def __str__(self):
        return self.code

class Customer(models.Model):
    customer_code = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    credit_limit = models.FloatField(null=True, blank=True)
    country = models.CharField(max_length=20, null=True, blank=True)
    class Meta:
        db_table = "customer"
        managed = False
    def __str__(self):
        return self.customer_code

class Invoice(models.Model):
    invoice_no = models.CharField(max_length=10, primary_key=True)
    date = models.DateField(null=True)
    customer_code = models.ForeignKey(Customer, on_delete=models.CASCADE, db_column='customer_code')
    due_date = models.DateField(null=True, blank=True)
    total = models.FloatField(null=True, blank=True)
    vat = models.FloatField(null=True, blank=True)
    amount_due = models.FloatField(null=True, blank=True)
    class Meta:
        db_table = "invoice"
        managed = False
    def __str__(self):
        return self.invoice_no

class Payment_method(models.Model):
    payment_method = models.CharField(max_length=10, primary_key=True)
    description = models.CharField(max_length=100, null=True)
    class Meta:
        db_table = "payment_method"
        managed = False
    def __str__(self):
        return self.payment_method

class receipt(models.Model):
    receipt_no = models.CharField(max_length=10, primary_key=True)
    created_at = models.DateField(null=True, blank=True)
    customer_code = models.CharField(max_length=10, null=True)
    payment_method = models.CharField(max_length=10, null=True)
    payment_reference = models.CharField(max_length=100, null=True)
    total_recieved = models.FloatField(null=True)
    remarks = models.CharField(max_length=100, null=True)
    class Meta:
        db_table = "receipt"
        managed = False
    def __str__(self):
        return self.receipt_no

class receipt_line_item(models.Model):
    receipt_no = models.CharField(max_length=10, primary_key=True)
    item_no = models.IntegerField()
    invoice_no = models.CharField(max_length=10, null=True)
    amount_paid_here = models.FloatField(null=True)
    class Meta:
        db_table = "receipt_line_item"
        managed = False
    def __str__(self):
        return self.receipt_no

class InvoiceLineItem(models.Model):
    invoice_no = models.ForeignKey(Invoice, primary_key=True, on_delete=models.CASCADE, db_column='invoice_no')
    item_no = models.IntegerField()
    product_code = models.ForeignKey(Product, on_delete=models.CASCADE, db_column='product_code')
    quantity = models.IntegerField(null=True)
    unit_price = models.FloatField(null=True)
    product_total = models.FloatField(null=True)
    class Meta:
        db_table = "invoice_line_item"
        unique_together = (("invoice_no", "item_no"),)
        managed = False
    def __str__(self):
        return '{"invoice_no":"%s","iten_no":"%s","product_code":"%s","product_name":"%s","quantity":%s,"unit_price":"%s","product_total":"%s"}' % (self.invoice_no, self.item_no, self.product_code, self.product_code.name, self.quantity, self.unit_price, self.product_total)

