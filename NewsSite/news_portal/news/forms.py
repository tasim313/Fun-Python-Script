from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'আপনার মন্তব্য লিখুন...',
                'rows': 4
            })
        }
        labels = {
            'body': 'মন্তব্য'
        }