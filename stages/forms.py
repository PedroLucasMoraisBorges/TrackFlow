from django import forms
from .models import *

class RegisterMilestone(forms.ModelForm):
    name = forms.CharField(
    required = True,
    label = 'Nome',
    widget = forms.TextInput(attrs={
        'placeholder' : 'Nome do Projeto',
        'class' : ''
        })
    )

    description = forms.CharField(
        required=True,
        label='Descrição',
        widget=forms.Textarea(attrs={
            'placeholder' : 'Descrição do projeto',
            'class' : ''
        })
    )
    
    class Meta:
        model = Stage
        fields = ['name', 'description', 'is_final']