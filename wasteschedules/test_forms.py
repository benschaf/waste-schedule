from django.test import TestCase
from .forms import CommentForm

class TestAboutForm(TestCase):
    def test_comment_form_valid(self):
        form = CommentForm({'body': 'This is a test comment'})
        self.assertTrue(form.is_valid(), msg="Form is not valid")

    def test_comment_form_invalid(self):
        form = CommentForm({'body': ''})
        self.assertFalse(form.is_valid(), msg="body is empty but form is valid")
