from .models import Comment
from django import forms

class CommentForm(forms.ModelForm):
    """
    A form for creating or updating comments.

    This form allows users to create or update comments by providing a text area
    for entering the comment body.

    Attributes:
        body (CharField): The field for entering the comment body.
                          The body label was altered as well as the widget
                          height.

    Meta:
        model (Comment): The model associated with the form.
        fields (tuple): The fields to include in the form.
                        only the body field is included.
    """
    body = forms.CharField(label='Your comment:', widget=forms.Textarea(attrs={'rows': 4}))

    class Meta:
        model = Comment
        fields = ('body',)