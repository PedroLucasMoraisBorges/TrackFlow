from django import forms
from .models import *

class CommentForm(forms.ModelForm):
    text = forms.CharField(
        required=True,
        label='Comentário',
        widget=forms.Textarea(attrs={
            'placeholder' : 'Comentário',
            'class' : ''
        })
    )