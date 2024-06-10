from django.test import TestCase
from .forms import PostalCodeForm


class TestPostalCodeForm(TestCase):
    """
    Test case for the PostalCodeForm.
    """

    def test_postal_code_form_valid(self):
        """
        Test if the PostalCodeForm is valid when a valid postal code is
        provided.
        """
        form = PostalCodeForm({'postal_code': '12345'})
        self.assertTrue(form.is_valid(), msg="Form is not valid")

    def test_postal_code_form_invalid(self):
        """
        Test if the PostalCodeForm is invalid when the postal code is empty.
        """
        form = PostalCodeForm({'postal_code': ''})
        self.assertFalse(form.is_valid(),
                         msg="postal_code is empty but form is valid")
