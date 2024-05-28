from wasteschedules.models import PostalCode
from django import forms

class PostalCodeForm(forms.ModelForm):
    """
    A form for handling postal codes.

    This form is used to collect and validate postal codes.

    Attributes:
        postal_code (str): The postal code entered by the user.

    Methods:
        validate_unique(): Custom method to skip unique validation.
                           Unique validation is performed later on in the view
    """
    class Meta:
        model = PostalCode
        fields = ['postal_code']

    def validate_unique(self):
        pass