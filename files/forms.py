from django import forms
from .models import *

class RegisterFileForm(forms.ModelForm):
    file = forms.FileField(
        required=True,
        label='Upload de Arquivo',
        widget=forms.FileInput(attrs={
            'class' : '',
        })
    )
    
    class Meta:
        model = File
        fields = ['file']