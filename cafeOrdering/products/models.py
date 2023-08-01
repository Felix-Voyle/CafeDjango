from django.db import models

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, max_length=100)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    category = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name