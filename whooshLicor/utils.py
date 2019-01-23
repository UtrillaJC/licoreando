import time

from whoosh import index
from whoosh import sorting
from whoosh.qparser import QueryParser
from whoosh.query import FuzzyTerm
from whoosh.query.terms import MultiTerm
from whoosh.sorting import MultiFacet

#Range facets
#facet= getPrecioFacet()
#results = searcher.search(myquery, groupedby=facet)
#results.groups(), devuelve un diccionario con los grupos.
def getPrecioFacet(rango):
    inferior=rango[0]
    superior=rango[1]-inferior
    return sorting.RangeFacet("precioGroup", 0, 10000, [inferior,superior]) # 0-10€, 10-50€, 50-100€ y ya de 100 en 100.

def getGraduacionFacet(rango):
    inferior=rango[0]
    superior=rango[1]-inferior
    return sorting.RangeFacet("graduacion", 0, 100, [inferior, superior],hardend=True)


def faceta_enStock():
    faceta_enStock = sorting.FieldFacet('enStock', reverse = True)
    return faceta_enStock

def faceta_categoria():
    faceta_categoria = sorting.FieldFacet('categoria')
    return faceta_categoria

    
def agruparLista(groupDic):

    grupo={}
    keys = groupDic.keys()
    if not(groupDic):
        return None
    else:
        if 'precio' in keys and 'graduacion' in keys:
            precioFacet=getPrecioFacet(groupDic["precio"])
            graduacionFacet=getGraduacionFacet(groupDic["graduacion"])
            multifaceta = MultiFacet([precioFacet,graduacionFacet])
            grupo= {"precio/graduacion":multifaceta}
        elif 'precio' not in keys and 'graduacion' in keys:
            grupo= {'graduacion': getGraduacionFacet(groupDic["graduacion"])}
        elif 'precio' in keys and 'graduacion' not in keys:
            grupo= {'precio':getPrecioFacet(groupDic["precio"])}
    return grupo
        
def listarPorAtributo(busqueda="",categoria=[], order ="",groupDic={}, nElementosPagina=20, pagina=1):
    tam=0
    ix=index.open_dir("whooshLicor/licoresIndex")
    lista = []
    busqueda = busqueda.strip()
    with ix.searcher() as searcher:
        if(not(busqueda) and not(categoria)):
            query = QueryParser("titulo",ix.schema).parse("*")
        elif(not(busqueda) and categoria):
            query = QueryParser("titulo",ix.schema).parse("*") & queryCategoryGenerator(categoria)
        elif(busqueda and not(categoria)):
            query = querySearchGenerator(busqueda)
        elif(busqueda and categoria):
            query = querySearchGenerator(busqueda) & queryCategoryGenerator(categoria)
        
        query.normalize()
        if not order:
            order = sorting.ScoreFacet()
        groupMap= agruparLista(groupDic)
        results = searcher.search(query,groupedby = groupMap,sortedby=[faceta_enStock(),order],limit = 4000)
        grupo = range(0,searcher.doc_count())
        tam=len(results)
        if(groupMap):
            try:
                if "precio/graduacion" in groupMap.keys():
                    tuplaKey=(groupDic["precio"],groupDic["graduacion"])
                elif("precio" in groupMap.keys()):
                    tuplaKey=groupDic["precio"]
                else:
                    tuplaKey=groupDic["graduacion"]
                    
                grupo=results.groups(next(iter(groupMap)))[tuplaKey]
            except:
                grupo=[]
    
            for documentIndex in grupo[(pagina-1)*nElementosPagina:pagina*nElementosPagina]:
                elemento = searcher.stored_fields(documentIndex)
                lista.append(elemento['id'])
            tam=len(grupo)
        elif not(groupDic):
            for r in results[(pagina-1)*nElementosPagina:pagina*nElementosPagina]:
                lista.append(r['id'])
        return (lista,tam)
        
def querySearchGenerator(busqueda):
    trozos = busqueda.split(" ")
    query = None
    for p in trozos:
        if(query is None):
            query = FuzzyTerm("titulo",p,maxdist=int(len(p)/4)) | FuzzyTerm("descripcion",p,maxdist=int(len(p)/4))
        else:
            query = query | FuzzyTerm("titulo",p,maxdist=int(len(p)/4)) | FuzzyTerm("descripcion",p,maxdist=int(len(p)/4))
    return query

def queryCategoryGenerator(busqueda):
    trozos = []
    
    for b in busqueda:
        t=[]
    
        if " " in b:
            t = b.split(" ")
            trozos = trozos + t
        elif "/" in b:
            t = b.split("/")
            trozos = trozos + t
            
        trozos.append(b)
    
    query = None
    
    for p in trozos:
        if(query is None):
            query = FuzzyTerm("categoria",p,maxdist=2)
        else:
            query = query | FuzzyTerm("categoria",p,maxdist=2)
    return query

#print(listarPorAtributo(nElementosPagina=10,pagina=1))
                
