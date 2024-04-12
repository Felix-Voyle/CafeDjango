from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages
from unittest.mock import patch
from .models import Enquiry
from . import views

class EnquireViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_submit_valid_enquiry_form(self):
        valid_data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'message': 'Test message',
            'phone_number': '1234567890',
            'subject': 'Test Subject'
        }

        response = self.client.post(reverse('enquire'), data=valid_data, follow=True)

        self.assertTrue(Enquiry.objects.filter(name='John Doe', email='john@example.com').exists())

        self.assertContains(response, 'Enquiry sent successfully!')
        self.assertRedirects(response, '/')

    def test_submit_invalid_enquiry_form(self):
        invalid_data = {}  # Invalid data intentionally left empty

        response = self.client.post(reverse('enquire'), data=invalid_data, follow=True)

        self.assertContains(response, 'The form you submitted was invalid')
        self.assertTemplateUsed(response, 'enquire/enquire.html')


    def test_enquire_view_handles_exception(self):
    # Simulate an exception being raised during form processing
        with patch('enquire.forms.EnquiryForm.save') as mock_save:
            mock_save.side_effect = Exception("Test exception: form save failed")

            # Construct a POST request with valid data
            data = {
                'name': 'Test User',
                'email': 'test@example.com',
                'message': 'Test message',
                'phone_number': '1234567890',
                'subject': 'Test Subject'
            }

            # Post the data to the view
            response = self.client.post(reverse('enquire'), data, follow=True)

        # Assert that the response status code is 500
        self.assertEqual(response.status_code, 500)
