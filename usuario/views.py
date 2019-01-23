from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from licor.models import Licor
from recomendaciones.recomendaciones import generaRecomendaciones
from usuario.forms import Registro, Login, FormularioPreferencias
from usuario.models import Formulario, PuntuacionCategoriaLicor, \
    PuntuacionOrigenLicor, PuntuacionMarcaLicor, Recomendaciones


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
            formulario = Formulario.objects.create(comentario=None,precioMinimo=None,precioMaximo=None,graduacionMinima=None,graduacionMaxima=None,usuario=user)
            return redirect('/user/login')
        return render(request,'register.html', {'form':form})
    return render(request,'register.html', {'form':form})

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

def formularios(request):
    user = request.user
    formulario = Formulario.objects.get(usuario=user)
    form = FormularioPreferencias(initial={'precioMinimo': formulario.precioMinimo,'precioMaximo': formulario.precioMaximo,'graduacionMinima': formulario.graduacionMinima,'graduacionMaxima': formulario.graduacionMaxima,'comentario': formulario.comentario})
    catLicor = PuntuacionCategoriaLicor.objects.filter(formulario=formulario)
    marcaLicor = PuntuacionMarcaLicor.objects.filter(formulario=formulario)
    origenLicor = PuntuacionOrigenLicor.objects.filter(formulario=formulario)
    if request.method=='POST':
        form = FormularioPreferencias(request.POST)
        if form.is_valid():
            comentario = form.cleaned_data['comentario']
            precioMinimo = form.cleaned_data['precioMinimo']
            precioMaximo = form.cleaned_data['precioMaximo']
            graduacionMinima = form.cleaned_data['graduacionMinima']
            graduacionMaxima = form.cleaned_data['graduacionMaxima']
            formulario.comentario=comentario
            formulario.precioMinimo=precioMinimo
            formulario.precioMaximo=precioMaximo
            formulario.graduacionMinima=graduacionMinima
            formulario.graduacionMaxima=graduacionMaxima
            formulario.save()
            licor = form.cleaned_data['licor']
            puntuacionL = form.cleaned_data['puntuacionLicor']
            if (licor and puntuacionL):  
                puntuacionLicor = PuntuacionCategoriaLicor.objects.create(licor=licor,puntuacion=puntuacionL,formulario=formulario)             
            origen = form.cleaned_data['origen']
            puntuacionO = form.cleaned_data['puntuacionOrigen']
            if (origen and puntuacionO):  
                puntuacionOrigen = PuntuacionOrigenLicor.objects.create(origen=origen,puntuacion=puntuacionO,formulario=formulario)
            marca =form.cleaned_data['marca']
            puntuacionM = form.cleaned_data['puntuacionMarca']
            if (marca and puntuacionM):  
                puntuacionMarca = PuntuacionMarcaLicor.objects.create(marca=marca,puntuacion=puntuacionM,formulario=formulario)
            
            generaRecomendaciones(formulario.id)
            return redirect("/user/forms")
        return render(request,'forms.html', {'form':form})
    return render(request,'forms.html', {'form':form,"catLicor":catLicor,"marcaLicor":marcaLicor,"origenLicor":origenLicor})

def recomendaciones(request):
    user = request.user
    formulario = Formulario.objects.get(usuario=user)
    recomendaciones = Recomendaciones.objects.filter(formulario=formulario)
    licores = []
    for r in recomendaciones:
        licores.append(Licor.objects.get(id=r.recomendado))
    return render(request,'recomendation.html',{'licores':licores})

@login_required
def logoutUsuario(request):
    logout(request)
    return render(request,'index.html')
