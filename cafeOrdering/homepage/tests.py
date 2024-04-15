from django.test import TestCase, RequestFactory
from django.shortcuts import render
from unittest.mock import patch
from .views import homepage

class HomepageViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    @patch.dict('os.environ', {'GOOGLE_MAPS_API_KEY': 'TEST_API_KEY'})
    def test_homepage_view(self):
        request = self.factory.get('/')

        response = homepage(request)

        self.assertEqual(response.status_code, 200)

