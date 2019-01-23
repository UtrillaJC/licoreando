import django
django.setup()
from licor.models import Licor,Categoria
from licor.scraping_casalicores import extraer_texto_casalicores
from licor.scraping_disevil import extraer_texto_disevil
from licor.scraping_marianomadrueno import extraer_licores


def save_all_licores():
    
    licores3 = extraer_licores()
    for licDicc in (licores3):
        print(licDicc)
        save_licor(licDicc)
    
    licores2 = extraer_texto_disevil() 
    for licDicc in (licores2):
        print(licDicc)
        save_licor(licDicc)
    
    licores = extraer_texto_casalicores()
    for licDicc in (licores):
        print(licDicc)
        save_licor(licDicc)
    

def save_licor(licDicc):
    licorAux = Licor.objects.filter(urlProducto = licDicc["urlProducto"]).first()
    if not licorAux:
        licorAux = Licor(codigoReferencia=licDicc["codigoReferencia"],
                      titulo=licDicc["titulo"],
                      descripcion=licDicc["descripcion"],
                      precio=licDicc["precio"],
                      origen=licDicc["origen"],
                      cantidad=licDicc["cantidad"],
                      graduacion=licDicc["graduacion"],
                      urlProducto=licDicc["urlProducto"],
                      urlImagen=licDicc["urlImagen"],
                      enStock=licDicc["enStock"],
                      )
        licorAux.save()


    for cat in licDicc["categoria"]:
        
        categoria = None
        try:
            categoria = Categoria(nombre=cat)
            categoria.save()
        except:
            categoria=Categoria.objects.filter(nombre = cat).first()
        categoria.licor.add(licorAux)
        
save_all_licores()