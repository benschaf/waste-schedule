from .models import Comment
from django import forms

class CommentForm(forms.ModelForm):
    # -> Credit for changing form widgets: https://docs.djangoproject.com/en/5.0/ref/forms/widgets/
    body = forms.CharField(label='Your comment:', widget=forms.Textarea(attrs={'rows': 4}))

    class Meta:
        model = Comment
        fields = ('body',)