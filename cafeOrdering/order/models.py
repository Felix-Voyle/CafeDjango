import uuid
from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User
from products.models import Product

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='OrderItem')
    address_line1 = models.CharField(max_length=100)
    address_line2 = models.CharField(max_length=100, blank=True, null=True)
    address_line3 = models.CharField(max_length=100, blank=True, null=True)
    postcode = models.CharField(max_length=10)
    delivery_instructions = models.TextField(blank=True, null=True)
    order_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    order_number = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  

    def _generate_order_number(self):
        return uuid.uuid4().hex.upper()
    
    def update_total(self):
        """
        Update total each time a line item is added.
        """
        self.order_total = self.order_items.all().aggregate(Sum('product__price'))['product__price__sum'] or 0
        print(self.order_total)

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self._generate_order_number()

        super(Order, self).save(*args, **kwargs)
        print(f"Updating total for Order {self.order_number}: New Total={self.order_total}")
        self.update_total()  

    def __str__(self):
        return f"Order #{self.order_number} for {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.order} - {self.product.name} x {self.quantity}"

