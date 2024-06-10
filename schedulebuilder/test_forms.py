from django.test import TestCase
from .forms import PostalCodeForm


class TestPostalCodeForm(TestCase):
    def test_postal_code_form_valid(self):
        form = PostalCodeForm({'postal_code': '12345'})
        self.assertTrue(form.is_valid(), msg="Form is not valid")

    def test_postal_code_form_invalid(self):
        form = PostalCodeForm({'postal_code': ''})
        self.assertFalse(form.is_valid(), msg="postal_code is empty but form is valid")
