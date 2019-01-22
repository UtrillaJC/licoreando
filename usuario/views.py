from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from usuario.forms import Registro, Login, FormularioPreferencias
from usuario.models import Formulario, PuntuacionCategoriaLicor, \
    PuntuacionOrigenLicor, PuntuacionMarcaLicor


def registro(request):
    form = Registro()
    if request.method=='POST':
        form = Registro(request.POST)
        if form.is_valid():
            username = form.cleaned_data['Username']
            name = form.cleaned_data['Nombre']
            last_name = form.cleaned_data['Apellido']
            email = form.cleaned_data['Email']
            passw = form.cleaned_data['Contraseña1']
            user = User.objects.create_user(username=username,password=passw,email=email,first_name=name,last_name=last_name)
            formulario = Formulario.objects.create(comentario="",precioMinimo="",precioMaximo="",graduacionMinima="",graduacionMaxima="",usuario=user)
            return redirect('/user/login')
        return render(request,'register.html', {'form':form})
    return render(request,'register.html', {'form':form})

def formularios(request):
    return render(request,'index.html')

def loginUsuario(request):
    form = Login()
    error = 'Error al hacer login, intentelo de nuevo o en caso de un fallo continuado, pongase en contacto con el administrador'
    if request.method=='POST':
        form = Login(request.POST)
        if form.is_valid():
            username = form.cleaned_data['usuario']
            password = form.cleaned_data['contraseña']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return render(request,'index.html')
            else:
                form = Login()
                return render(request,'login.html',{'form':form, "error":error})
        return render(request,'login.html', {'form':form,'error':error})
    return render(request,'login.html', {'form':form})

def formularioPreferencias(request):
    form = FormularioPreferencias()
    if request.method=='POST':
        form = FormularioPreferencias(request.POST)
        if form.is_valid():
            comentario = form.cleaned_data['comentario']
            precioMinimo = form.cleaned_data['precioMinimo']
            precioMaximo = form.cleaned_data['precioMaximo']
            graduacionMinima = form.cleaned_data['graduacionMinima']
            graduacionMaxima = form.cleaned_data['graduacionMinima']
            user = request.user
            formulario = Formulario.objects.get(ususario=user)
            formulario = Formulario.objects.create(id = formulario.id,  comentario=comentario,precioMinimo=precioMinimo,precioMaximo=precioMaximo,graduacionMinima=graduacionMinima,graduacionMaxima=graduacionMaxima,usuario=user)
            return render(request,'index.html')
        return render(request,'forms.html', {'form':form})
    return render(request,'forms.html', {'form':form})

def formularioLicor(request):
    form = formularioLicor()
    if request.method=='POST':
        form = formularioLicor(request.POST)
        if form.is_valid():
            user = request.user
            formulario = Formulario.objects.get(ususario=user)
            licor = form.cleaned_data['licor']
            puntuacion = form.cleaned_data['puntuacion']
            puntuacionCategoriaLicor =PuntuacionCategoriaLicor.objects.create(formulario=formulario,puntuacion=puntuacion,licor=licor)
            return render(request,'forms.html')
        return render(request,'forms.html', {'form':form})
    return render(request,'forms.html', {'form':form})

def formularioOrigen(request):
    form = formularioLicor()
    if request.method=='POST':
        form = formularioLicor(request.POST)
        if form.is_valid():
            user = request.user
            formulario = Formulario.objects.get(ususario=user)
            origen = form.cleaned_data['origen']
            puntuacion = form.cleaned_data['puntuacion']
            puntuacionOrigenLicor =PuntuacionOrigenLicor.objects.create(formulario=formulario,puntuacion=puntuacion,origen=origen)
            return render(request,'forms.html')
        return render(request,'forms.html', {'form':form})
    return render(request,'forms.html', {'form':form})

def formularioMarca(request):
    form = formularioLicor()
    if request.method=='POST':
        form = formularioLicor(request.POST)
        if form.is_valid():
            user = request.user
            formulario = Formulario.objects.get(ususario=user)
            marca =form.cleaned_data['marca']
            puntuacion = form.cleaned_data['puntuacion'] 
            puntuacionMarcaLicor = PuntuacionMarcaLicor.objects.create(formulario=formulario,puntuacion=puntuacion,marca=marca)
            return render(request,'forms.html')
        return render(request,'forms.html', {'form':form})
    return render(request,'forms.html', {'form':form})

@login_required
def logoutUsuario(request):
    logout(request)
    return render(request,'index.html')
