from django.shortcuts import render
from django.template.defaultfilters import lower

from licor.forms import SearchForm
from licor.models import Licor, Categoria
from whooshLicor.utils import listarPorAtributo

def index(request): 
    return render(request,'index.html')

def buscarLicor(request):
    form=SearchForm()
    categorias = Categoria.objects.all().order_by('nombre')
    if request.method=='POST':
        form = SearchForm(request.POST, request.FILES)
        if form.is_valid():
            busqueda = form.cleaned_data["busqueda"]
            graduacionMinima = form.cleaned_data["graduacionMinima"]
            graduacionMaxima = form.cleaned_data["graduacionMaxima"]
            precioMinimo = form.cleaned_data["precioMinimo"]
            precioMaximo = form.cleaned_data["precioMaximo"]
            elem = request.POST["elem"]
            page = request.POST["page"]
            groupDic={}
            if precioMinimo and precioMaximo:
                groupDic["precio"]=(precioMinimo,precioMaximo)
            if graduacionMinima and graduacionMaxima:
                groupDic["graduacion"]=(graduacionMinima,graduacionMaxima)
            orden = request.POST["order"]
            categoriaP = request.POST.getlist("categoria")
            categoria = []
            for cat in categoriaP:
                categoria.append((Categoria.objects.get(id=cat)).nombre.lower())
            busqueda = lower(busqueda)       
            licoresId = listarPorAtributo(busqueda=busqueda,categoria=categoria, order =orden,groupDic=groupDic, nElementosPagina=int(elem), pagina=int(page))
            licores = getLicores(licoresId)
            return render(request,'search_licor.html', {'licores':licores,'form':form ,'categorias': categorias,'elem':elem,'page':page})
    licoresId = listarPorAtributo()
    licores = getLicores(licoresId)
    return render(request,'search_licor.html', {'form':form,'licores':licores, 'categorias': categorias,'elem':20,'page':1})

def getLicores(licoresId):
    licores = []
    for licor in licoresId[0]:
        licores.append(Licor.objects.get(id=licor)) 
    return licores
