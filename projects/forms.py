from django import forms
from.models import *
from auth_user.models import *
from django.utils.timezone import now

class RegisterProjectForm(forms.ModelForm):
    name = forms.CharField(
        required=True,
        label='Nome',
        widget=forms.TextInput(attrs={
            'placeholder': 'Nome do Projeto',
            'class': ''
        })
    )

    description = forms.CharField(
        required=True,
        label='Descrição',
        widget=forms.Textarea(attrs={
            'placeholder': 'Descrição do projeto',
            'class': ''
        })
    )

    fk_owner = forms.ModelChoiceField(
        required=True,
        label='Cliente',
        queryset=User.objects.none(),
        widget=forms.Select(attrs={
            'class': ''
        })
    )

    dt_init = forms.DateField(
        required=False,
        label='Data de início do projeto',
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'min': now().date().isoformat(),  # <--- Define o mínimo como hoje
                'class': ''
            }
        )
    )

    time_interval = forms.IntegerField(
        required=False,
        label='Intervalo de tempo'
    )

    def clean(self):
        cleaned_data = super().clean()
        dt_init = cleaned_data.get('dt_init')
        time_interval = cleaned_data.get('time_interval')

        if time_interval and not dt_init:
            self.add_error('dt_init', 'Se o intervalo de tempo for definido, a data de início é obrigatória.')


    class Meta:
        model = Project
        fields = ['name', 'description', 'fk_owner', 'dt_init', 'time_interval']

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

    dt_init = forms.DateField(
        required=False,
        label='Data de início do projeto',
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'min': now().date().isoformat(),  # <--- Define o mínimo como hoje
                'class': ''
            }
        )
    )

    time_interval = forms.IntegerField(
        required=False,
        label='Intervalo de tempo'
    )

    def clean(self):
        cleaned_data = super().clean()
        dt_init = cleaned_data.get('dt_init')
        time_interval = cleaned_data.get('time_interval')

        if time_interval and not dt_init:
            self.add_error('dt_init', 'Se o intervalo de tempo for definido, a data de início é obrigatória.')

    class Meta:
        model = Project
        fields = ['name', 'description', 'dt_init', 'time_interval',] 

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
    
class CreateProjectWithAiForm(forms.Form):
    description = forms.CharField(
        required=True,
        label='Descrição do Projeto',
        widget=forms.Textarea(attrs={'id' : 'description_for_ai'})
    )

    owner = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=True,
        label='Cliente',
        widget=forms.Select(attrs={'id' : 'owner'})
    )

    def __init__(self, *args, **kwargs):
        manager = kwargs.pop("manager", None)
        super(CreateProjectWithAiForm, self).__init__(*args, **kwargs)

        if manager:
            manager = User.objects.get(id=manager.id)
            self.fields['owner'].queryset = manager.clients.all()

class RateTemplateForm(forms.ModelForm):
    choices = [
        (0.0, 0.0),
        (0.5, 0.5),
        (1.0, 1.0),
        (1.5, 1.5),
        (2.0, 2.0),
        (2.5, 2.5),
        (3.0, 3.0),
        (3.5, 3.5),
        (4.0, 4.0),
        (4.5, 4.5),
        (5.0, 5.0),
    ]
    rate = forms.ChoiceField(
        choices=choices,
        label='Nota',
        widget=forms.Select()
    )

    class Meta:
        model = Evaluation
        fields = ['rate']