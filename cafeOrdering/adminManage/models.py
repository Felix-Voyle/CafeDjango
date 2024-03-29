import random

from django.db import models


class manageInvoice(models.Model):
    invoice_id = models.CharField(max_length=5, unique=True)
    invoice_date = models.DateField()
    invoice_sent_date = models.DateField(auto_now_add=True)
    invoice_total = models.DecimalField(max_digits=10, decimal_places=2)
    invoice_paid = models.BooleanField(default=False)

    @staticmethod
    def generate_invoice_id():
        retry_limit = 5
        for _ in range(retry_limit):
            invoice_id = ''.join(random.choices('0123456789', k=5))
            if not manageInvoice.objects.filter(invoice_id=invoice_id).exists():
                return invoice_id
        raise ValueError("Failed to generate a unique order ID after {} retries.".format(retry_limit))
    
    
    def __str__(self):
        return f"Invoice ID: {self.invoice_id}, Invoice Date: {self.invoice_date}, Total: {self.invoice_total}, Paid: {self.paid}"

