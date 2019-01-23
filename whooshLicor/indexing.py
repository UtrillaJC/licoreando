from _decimal import Decimal
import os
import django
django.setup()
from django.core.paginator import Paginator
from whoosh import index
from licor.models import Licor
from whooshLicor.schemas import crear_esquema

def indexar():
    if not os.path.exists("licoresIndex"):
        os.mkdir("licoresIndex")
    
    index.create_in("licoresIndex", crear_esquema())
    

    ix = index.open_dir("licoresIndex")
    writer = ix.writer()
    
    licores = Licor.objects.all().order_by('id')
    
    
    paginator = Paginator(licores, 20)
    
    licores = paginator.page(1)
    while licores.has_next():
        for licor in licores:
            i = licor.id
            t = licor.titulo.strip()
            d = licor.descripcion
            if not(licor.precio):
                p=None
                pGroup = None
            else:
                p = licor.precio
                pGroup = p 
                p=Decimal(str(p))
            o = licor.origen
            if not(licor.graduacion):
                grad = None
            else:
                grad = licor.graduacion
            es = licor.enStock
            url = licor.urlProducto
            cat = array_toString(list(licor.categoria_set.all()))
            print(cat)
            writer.add_document(id= i, categoria = cat,titulo = t,descripcion = d,precio = p, precioGroup= pGroup,
                                origen = o,graduacion = grad, enStock= es,urlProducto=url)
       
        licores = paginator.page(licores.next_page_number())
    writer.commit()

def array_toString(array):
    result = ""
    for a in array:
        result= result + str(a.nombre) + " "
    return result
indexar()
    