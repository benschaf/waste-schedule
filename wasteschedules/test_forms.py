from django.test import TestCase
from .forms import CommentForm


class TestAboutForm(TestCase):
    """
    A test case for the CommentForm class.

    This test case verifies the behavior of the CommentForm class by testing
    the validity of the form with both valid and invalid input data.
    """

    def test_comment_form_valid(self):
        """
        Test that the CommentForm is valid when the body is not empty.
        """
        form = CommentForm({'body': 'This is a test comment'})
        self.assertTrue(form.is_valid(), msg="Form is not valid")

    def test_comment_form_invalid(self):
        """
        Test that the CommentForm is invalid when the body is empty.
        """
        form = CommentForm({'body': ''})
        self.assertFalse(
            form.is_valid(), msg="body is empty but form is valid")
