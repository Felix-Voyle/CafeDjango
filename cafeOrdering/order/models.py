import random
import string
from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User
from django.utils import timezone
from products.models import Product

class Order(models.Model):

    ORDER_STATUS = (
        ('ordered', 'Ordered'),
        ('sent', 'Sent'),
        ('invoiced', 'Invoiced'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='OrderItem')
    address_line1 = models.CharField(max_length=100)
    address_line2 = models.CharField(max_length=100, blank=True, null=True)
    address_line3 = models.CharField(max_length=100, blank=True, null=True)
    postcode = models.CharField(max_length=10)
    delivery_instructions = models.TextField(max_length=150, blank=True, null=True)
    delivery_date = models.DateField()
    delivery_time = models.TimeField()
    order_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    order_id = models.TextField(max_length=5, editable=False, unique=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='ordered')
    reported_problem = models.TextField(max_length=200, blank=True, null=True)


    def _generate_order_id(self):
        retry_limit = 5
        for _ in range(retry_limit):
            order_id = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
            if not Order.objects.filter(order_id=order_id).exists():
                return order_id
        raise ValueError("Failed to generate a unique order ID after {} retries.".format(retry_limit))
    
    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = self._generate_order_id()

        super(Order, self).save(*args, **kwargs)
    
    def update_total(self):
        """
        Update total each time a line item is added.
        """
        order_items = self.order_items.all()
        total = sum(item.get_total() for item in order_items)
        self.order_total = total
        self.save()
        
    def finalize_order(self):
        self.update_total()
    

    def is_reportable(self):
        """
        Check if the order can be reported for problems within 24 hours of the delivery date and time.
        """
        # Calculate the current datetime
        current_datetime = timezone.now()

        # Combine the delivery date and time into a single datetime object
        delivery_datetime = timezone.datetime.combine(self.delivery_date, self.delivery_time)

        # Calculate the difference between the current datetime and the delivery datetime
        time_difference = current_datetime - delivery_datetime
        
        # Check if the time difference is within 24 hours
        return time_difference.days == 0 and time_difference.seconds < 86400

    @property
    def reportable(self):
        """
        Property method to make it easier to access the reportable status in templates.
        """
        return self.is_reportable()

    def __str__(self):
        return f"Order #{self.order_id} for {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.order} - {self.product.name} x {self.quantity}"

