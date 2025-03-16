from django import forms
from .models import *

class RegisterMilestoneForm(forms.ModelForm):
    name = forms.CharField(
        required = True,
        label = 'Nome',
        widget = forms.TextInput(attrs={
            'placeholder' : 'Nome do marco',
            'class' : ''
        })
    )

    description = forms.CharField(
        required=True,
        label='Descrição',
        widget=forms.Textarea(attrs={
            'placeholder' : 'Descrição do marco',
            'class' : ''
        })
    )
    
    class Meta:
        model = Milestone
        fields = ['name', 'description']