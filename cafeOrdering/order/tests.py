from django.test import TestCase, RequestFactory
from django.contrib.messages.storage.fallback import FallbackStorage
from django.urls import reverse
from django.contrib.auth.models import User
from products.models import Product, Category
from .models import Order
from .views import order

class OrderViewTest(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='password')

        self.category = Category.objects.create(name='Test Category')
        self.product = Product.objects.create(name='Test Product', category=self.category, price=10.00)

        self.factory = RequestFactory()

    def test_order_view_post(self):
        # Create a request factory
        self.factory = RequestFactory()

        # Create a POST request with form data
        data = {
            'address_line1': '123 Test Street',
            'postcode': '12345',
            'confirmed-product': [self.product.id],
            'confirmed-qty': [1],
            'price': [self.product.price],
            'delivery_date': '2023-03-03',
            'delivery_time': "00:00:00",
        }
        request = self.factory.post(reverse('order'), data)
        request.user = self.user

        # Add middleware processing to the request
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        # Call the view function
        response = order(request)

        # Assertions
        self.assertEqual(response.status_code, 302)  # Redirect expected after successful order placement

    def test_order_view_get(self):
        # Create a GET request
        request = self.factory.get(reverse('order'))
        request.user = self.user

        # Call the view function
        response = order(request)

        # Assertions
        self.assertEqual(response.status_code, 200)

