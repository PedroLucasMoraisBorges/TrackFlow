from django import forms
from.models import *
from auth_user.models import *

class RegisterProjectForm(forms.ModelForm):
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


    fk_owner = forms.ModelChoiceField(
        required=True,
        label='Cliente',
        queryset=User.objects.none(),  # Definido como vazio inicialmente
        widget=forms.Select(attrs={
            'class': ''
        })
    )

    class Meta:
        model = Project
        fields = ['name', 'description', 'fk_owner']

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['fk_owner'].queryset = user.clients.all()

class RegisterUserProjectForm(forms.ModelForm):
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
        model = Project
        fields = ['name', 'description'] 

class EditProjectForm(forms.ModelForm):
    name = forms.CharField(
        required = False,
        label = 'Nome',
        widget = forms.TextInput(attrs={
            'placeholder' : 'Nome do Projeto',
            'class' : ''
        })
    )

    description = forms.CharField(
        required=False,
        label='Descrição',
        widget=forms.Textarea(attrs={
            'placeholder' : 'Descrição do projeto',
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
        model = Project
        fields = ['name', 'description'] 