from django.test import TestCase, RequestFactory
from django.contrib.messages.storage.fallback import FallbackStorage
from django.urls import reverse
from django.contrib.auth.models import User
from products.models import Product, Category
from .models import Order
from .views import order

class OrderViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')

        self.category = Category.objects.create(name='Test Category')
        self.product = Product.objects.create(name='Test Product', category=self.category, price=10.00)

        self.factory = RequestFactory()

    def test_order_view_post(self):
        self.factory = RequestFactory()

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

        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = order(request)

        self.assertEqual(response.status_code, 302) 

    def test_order_view_get(self):
        request = self.factory.get(reverse('order'))
        request.user = self.user

        response = order(request)

        self.assertEqual(response.status_code, 200)

