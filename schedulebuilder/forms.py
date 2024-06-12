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
        """
        Attributes:
            model (Model): The model class associated with the form.
            fields (list): only the postal_code field is included in the form.
        """
        model = PostalCode
        fields = ["postal_code"]

    def validate_unique(self):
        """
        unique validation is performed later on in the view as the postal code
        should be unique in the database but the user can access an existing
        postal code.
        """
        pass
