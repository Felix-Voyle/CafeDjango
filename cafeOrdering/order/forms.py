from django.core.exceptions import ValidationError
from datetime import datetime
import re

def validate_order_form_data(data):
    # Perform validation for the order form data
    errors = {}

    # Validate address_line1
    address_line1 = data.get('address_line1')
    if not address_line1:
        errors['address_line1'] = 'Address line 1 is required.'
    if len(address_line1) > 100:
        errors['address_line1'] = "Address line 2 can't be longer than 100 characters."
    
    # Validate address_line2
    address_line2 = data.get('address_line2')
    if address_line2 and len(address_line2) > 100:
        errors['address_line2'] = "Address line 2 can't be longer than 100 characters."

    # Validate address_line3
    address_line3 = data.get('address_line3')
    if address_line3 and len(address_line3) > 100:
        errors['address_line3'] = "Address line 3 can't be longer than 100 characters."

    delivery_instructions = data.get('delivery_instructions')
    if delivery_instructions and len(delivery_instructions) > 150:
        errors['delivery_instructions'] = 'Delivery instructions cannot exceed 150 characters.'   

    # Validate postcode
    postcode = data.get('postcode')
    if not postcode:
        errors['postcode'] = 'Postcode is required.'
    if len(postcode) > 10:
        errors['postcode'] = "Postcode can't be longer than 10 characters"

    # Validate delivery_date (if required)
    delivery_date = data.get('delivery_date')
    if not delivery_date:
        errors['delivery_date'] = 'Delivery date is required.'
        try:
            datetime.strptime(delivery_date, '%Y-%m-%d')
        except ValueError:
            errors['delivery_date'] = 'Invalid date format.'

    # Validate delivery_time (if required)
    delivery_time = data.get('delivery_time')
    if not delivery_time:
        errors['delivery_time'] = 'Delivery time is required.'
    else:
        time_format = r'^([01]\d|2[0-3]):([0-5]\d)$'
    if not re.match(time_format, delivery_time):
        errors['delivery_time'] = 'Invalid time format. Please use HH:MM.'
    

    return errors