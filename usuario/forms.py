# -*- encoding: utf-8 -*-
from django import forms
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _


class Registro(forms.Form):
    Username = forms.CharField(required=False)
    Nombre = forms.CharField(max_length=30)
    Apellido = forms.CharField(max_length=60)
    Email = forms.CharField(required=False)
    Contraseña1 = forms.CharField(widget=forms.PasswordInput)
    Contraseña2 = forms.CharField(widget=forms.PasswordInput)
   
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('Username')
        password1 = cleaned_data.get('Contraseña1')
        password2 = cleaned_data.get('Contraseña2')

        if not password1 == password2:
            raise forms.ValidationError(
                _("La contraseña no coincide"),
                code='not_matching_passwords'
            )
        try:
            User.objects.get(username=username)
            raise forms.ValidationError(
                _("Ya existe un usuario con ese nombre"),
                code='username_must_unique')
        except ObjectDoesNotExist:
            pass


class Login(forms.Form):
    usuario = forms.CharField(max_length=30)
    contraseña = forms.CharField(max_length=30, widget=forms.PasswordInput)    
 
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('Usuario')
        password = cleaned_data.get('Contraseña')
        hashed_password = make_password(password)
        try:
            user = User.objects.filter(username=username, password=hashed_password)
        except ObjectDoesNotExist:
            raise forms.ValidationError(_("Esta cuenta no existe"),
                code='not_existent_account')
            
class FormularioPreferencias(forms.Form):
    precioMinimo = forms.FloatField(required=False, label="Precio Mínimo")
    precioMaximo = forms.FloatField(required=False,label="Precio Máximo")
    graduacionMinima = forms.FloatField(required=False,label="Graduación Mínima")
    graduacionMaxima = forms.FloatField(required=False,label="Graduación Máxima")
    comentario = forms.CharField(widget=forms.Textarea,required=False)

class FormularioLicor(forms.Form):
    licor = forms.CharField()
    puntuacion = forms.IntegerField(min_value=0, max_value=10)
    
class FormularioOrigen(forms.Form):
    origen = forms.CharField()
    puntuacion = forms.IntegerField(min_value=0, max_value=10)

class FormularioMarca(forms.Form):
    marca =forms.CharField()
    puntuacion = forms.IntegerField(min_value=0, max_value=10)
