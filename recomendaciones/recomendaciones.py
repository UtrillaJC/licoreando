'''
Created on 23 ene. 2019

@author: viento
'''
import django
from recomendaciones.distancia import getPuntuacionFrase, getPuntuacionRango,\
    getPuntuacionAtributo
django.setup()

from licor.models  import Licor, Categoria
from django.contrib.auth.models import User
from usuario.models import Formulario, PuntuacionCategoriaLicor, PuntuacionMarcaLicor, PuntuacionOrigenLicor, Recomendaciones


def generaRecomendaciones(idFormulario):
    form = Formulario.objects.filter(pk = idFormulario).first()
    if form:
        recomendacionesDict={}
        for licor in Licor.objects.all():
            recomendacionesDict.update(getPuntuacionLicor(form, licor))
        
        veinteMejores = sorted(recomendacionesDict.items(), key=lambda p: p[1],reverse=True)[0:20]
        print(veinteMejores)
        Recomendaciones.objects.filter(formulario=form).delete()
        for mejor in veinteMejores:
            Recomendaciones.objects.create(recomendado=mejor[0],formulario=form)
    else:
        return 0
    
    return 1

def getPuntuacionLicor(form,licor):
    puntuacion = 0.0

    if form.comentario and licor.descripcion:
        puntuacion=puntuacion+getPuntuacionFrase(form.comentario,licor.descripcion)
    if licor.precio and form.precioMinimo and form.precioMaximo:
        puntuacion=puntuacion+getPuntuacionRango(licor.precio,form.precioMinimo,form.precioMaximo)
    if licor.graduacion and form.graduacionMinima and form.graduacionMaxima:
        puntuacion=puntuacion+getPuntuacionRango(licor.graduacion,form.graduacionMinima,form.graduacionMaxima)
    
    for categoriaF in form.puntuacioncategorialicor_set.all():
        for categoriaL in licor.categoria_set.all():
            puntuacion=puntuacion+getPuntuacionAtributo(categoriaF.licor, categoriaL.nombre, categoriaF.puntuacion)
            
    for origenF in form.puntuacionorigenlicor_set.all():
        puntuacion=puntuacion+getPuntuacionAtributo(origenF.origen,licor.origen, origenF.puntuacion)
        
    for marcaF in form.puntuacionmarcalicor_set.all():
        puntuacion=puntuacion+getPuntuacionAtributo(marcaF.marca,licor.titulo, marcaF.puntuacion)
    
    return {licor.id:puntuacion}
    