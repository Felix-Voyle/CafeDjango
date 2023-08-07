from django.db import models
from django.contrib.auth.models import User
from users.models import UserProfile
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
    order_number = models.CharField(max_length=10, unique=True)  

    def save(self, *args, **kwargs):
        
        if not self.order_number:
            self.order_number = self._generate_order_number()

        self.order_total = sum(item.get_total() for item in self.order_items.all())
        super(Order, self).save(*args, **kwargs)

    def _generate_order_number(self):
        import time
        timestamp = int(time.time() * 1000)
        return f"{self.user.pk}-{timestamp}"

    def __str__(self):
        return f"Order #{self.order_number} for {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity} {self.product.name} in the order"
