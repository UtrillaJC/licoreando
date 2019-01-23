# -*- encoding: utf-8 -*-
from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.template.defaultfilters import default

from licor.models import Categoria


class SearchForm(forms.Form):
    busqueda = forms.CharField(required=False,label="Búsqueda")
    graduacionMinima = forms.FloatField(required=False,label="Graduación mínima",min_value=0,max_value=99)
    graduacionMaxima = forms.FloatField(required=False,label="Graduación máxima",min_value=0,max_value=99)
    precioMinimo = forms.FloatField(required=False,label="Precio mínimo",min_value=0,max_value=9999)
    precioMaximo = forms.FloatField(required=False,label="Precio máximo",min_value=0,max_value=9999)
    ordenarSimilitud = forms.RadioSelect()
    ordenarPrecio = forms.RadioSelect()
    ordenarTitulo = forms.RadioSelect()
    ordenarGraduacion = forms.RadioSelect()
    ordenarProcedencia = forms.RadioSelect()
    def clean(self):
        cleaned_data = super().clean()
        graduacionMinima = cleaned_data.get('Graduación mínima')
        graduacionMaxima = cleaned_data.get('Graduación máxima')
        precioMinimo = cleaned_data.get('Precio mínima')
        precioMaximo = cleaned_data.get('Precio máxima')
        nombre = cleaned_data.get('Categoría')
        try:
            if graduacionMinima > graduacionMaxima:
                raise forms.ValidationError(
                    _("La graduación mínima no puede ser superior a la graduación máxima"),
                    code='invalid'
                )
            if precioMinimo > precioMaximo:
                raise forms.ValidationError(
                    _("El precio mínimo no puede ser superior al precio máximo"),
                    code='invalid'
                )
        except:
            pass
