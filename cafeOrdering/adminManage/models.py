import random
import datetime
import io


from django.utils import timezone
from django.core.files.base import ContentFile

from django.db import models

class ManageInvoice(models.Model):
    invoice_reference = models.CharField(max_length=5, unique=True)
    invoice_date = models.DateField()
    invoice_sent_date = models.DateField(auto_now_add=True)
    invoice_total = models.DecimalField(max_digits=10, decimal_places=2)
    invoice_paid = models.BooleanField(default=False)
    invoice_pdf = models.BinaryField(blank=True, null=True)

    @staticmethod
    def generate_invoice_id():
        retry_limit = 5
        for _ in range(retry_limit):
            invoice_reference = ''.join(random.choices('0123456789', k=5))
            if not ManageInvoice.objects.filter(invoice_reference=invoice_reference).exists():
                return invoice_reference
        raise ValueError("Failed to generate a unique order ID after {} retries.".format(retry_limit))
    
    def __str__(self):
        return f"Invoice Reference: {self.invoice_reference}, Invoice Date: {self.invoice_date}, Total: {self.invoice_total}, Paid: {self.invoice_paid}"
    

    def is_due(self):
        due_date = timezone.make_aware(datetime.datetime.combine(self.invoice_date, datetime.time.min)) + timezone.timedelta(days=30)
        
        return timezone.now() > due_date
    

    @property
    def due(self):
        return self.is_due()
