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

    
class EditMilestoneForm(forms.ModelForm):
    name = forms.CharField(
        required = False,
        label = 'Nome',
        widget = forms.TextInput(attrs={
            'placeholder' : 'Nome do marco',
            'class' : ''
        })
    )

    description = forms.CharField(
        required=False,
        label='Descrição',
        widget=forms.Textarea(attrs={
            'placeholder' : 'Descrição do marco',
            'class' : ''
        })
    )

    def save(self, commit=True, instance=None):
        """Salva apenas os campos preenchidos no formulário."""
        if instance is None:
            instance = super().save(commit=False)
        else:
            for field in self.cleaned_data:
                value = self.cleaned_data[field]
                if value:
                    setattr(instance, field, value)

        if commit:
            instance.save()
        return instance
    
    class Meta:
        model = Milestone
        fields = ['name', 'description']