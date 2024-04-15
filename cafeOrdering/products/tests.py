from django.test import TestCase
from .models import Category, Product

class ProductModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Category.objects.create(name='Test Category')

    def setUp(self):
        # Set up modified objects used by test methods
        self.category = Category.objects.get(name='Test Category')

    def test_product_creation(self):
        product = Product.objects.create(
            price=10.50,
            name='Test Product',
            description='Test description',
            category=self.category
        )
        self.assertEqual(product.price, 10.50)
        self.assertEqual(product.name, 'Test Product')
        self.assertEqual(product.description, 'Test description')
        self.assertEqual(product.category, self.category)
