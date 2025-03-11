from django import forms
from .models import *

class RegisterFile(forms.ModelForm):
    file = forms.FileField(
        required=True,
        label='Upload de Arquivo',
        widget=forms.FileInput(attrs={
            'class' : ''
        })
    )

    type = forms.ChoiceField(
        required=True,
        choices=[('' , 'Selecione um Tipo')] + doc_types,
        label='Tipo de arquivo',
        widget=forms.Select(attrs={
            'class' : ''
        })
    )
    
    class Meta:
        model = File
        fields = ['file', 'type']