from typing import Any, Mapping
from django import forms
from django.contrib.auth import authenticate
from django.forms.renderers import BaseRenderer
from django.forms.utils import ErrorList

from .models import User

class UserRegisterForm(forms.ModelForm):
    """Form definition for User."""

    password1 = forms.CharField(
        label='contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder':'Inserte contraseña'
            }
        )
    )

    password2 = forms.CharField(
        label='contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder':'Repetir contraseña'
            }
        )
    )

    class Meta:
        """Meta definition for Userform."""

        model = User
        fields = (
            'username',
            'email',
            'nombres',
            'apellidos',
            'genero',
        )

    def clean_password2(self):
        if self.cleaned_data['password1'] != self.cleaned_data['password2']:
            self.add_error('password2', 'Las contraseñas no son iguales')

class LoginForm(forms.Form):
    username = forms.CharField(
        label='username',
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'username',
                'style':'{ margin: 10px }',
            }
        )
    )
    password = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder':'Inserte contraseña'
            }
        )
    )

    def clean(self):
        cleaned_data = super().clean()
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        if not authenticate(username=username, password=password):
            raise forms.ValidationError('Los datos de usuarios no son correctos')
        
        return self.cleaned_data

class PasswordUpdateForm(forms.Form):
    password1 = forms.CharField(
        label='contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder':'Inserte contraseña actual'
            }
        )
    )

    password2 = forms.CharField(
        label='contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder':'Inserte contraseña nueva'
            }
        )
    )

class VerificationForm(forms.Form):
    codregistro = forms.CharField(required=True)

    def __init__(self, pk, *args, **kwargs):
        self.id_user = pk
        super().__init__(*args, **kwargs)

    def clean_codregistro(self):
        codigo = self.cleaned_data['codregistro']

        if len(codigo) == 6:
            activo = User.objects.cod_validation(
                # self.kwargs['pk'], esto es cuando trabajamos con vistas
                self.id_user,
                codigo,
            )
            if not activo:
                raise forms.ValidationError('Codigo incorrecto')
        else:
            raise forms.ValidationError('Codigo incorrecto')