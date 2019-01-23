from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

# Create your models here.
class Formulario(models.Model):
    usuario = models.OneToOneField(User, blank = False, null = False, on_delete= models.CASCADE)
    comentario = models.TextField(blank = True, null = True)
    precioMinimo = models.FloatField(blank = True, null = True)
    precioMaximo = models.FloatField(blank = True, null = True)
    graduacionMinima = models.FloatField(blank = True, null = True)
    graduacionMaxima = models.FloatField(blank = True, null = True)

class Recomendaciones(models.Model):
    recomendado = models.IntegerField(blank = False, null = False)
    formulario = models.ForeignKey(Formulario,blank = False, null = False, on_delete = models.CASCADE)
    
class PuntuacionCategoriaLicor(models.Model):
    licor = models.TextField()
    puntuacion = models.IntegerField(validators= [MinValueValidator(0), MaxValueValidator(10)])
    formulario = models.ForeignKey(Formulario,blank = False, null = False, on_delete = models.CASCADE)
    
class PuntuacionOrigenLicor(models.Model):
    origen = models.TextField()
    puntuacion = models.IntegerField(validators= [MinValueValidator(0), MaxValueValidator(10)])
    formulario = models.ForeignKey(Formulario,blank = False, null = False, on_delete = models.CASCADE)

class PuntuacionMarcaLicor(models.Model):
    marca =models.TextField()
    puntuacion = models.IntegerField(validators= [MinValueValidator(0), MaxValueValidator(10)])
    formulario = models.ForeignKey(Formulario,blank = False, null = False, on_delete = models.CASCADE)
