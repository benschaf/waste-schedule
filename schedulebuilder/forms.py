from wasteschedules.models import PostalCode, validate_postal_code
from django import forms

class PostalCodeForm(forms.ModelForm):
    class Meta:
        model = PostalCode
        fields = ['postal_code']

    def validate_unique(self):
        pass