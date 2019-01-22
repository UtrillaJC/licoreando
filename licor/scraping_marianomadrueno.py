from bs4 import BeautifulSoup
import urllib.request
import time
import re

def abrir_url(url):
    r = urllib.request.urlopen(url)
    return r


def numero_paginas(url='https://marianomadrueno.es/tienda/'):
    soupAux = BeautifulSoup(abrir_url(url),'html.parser')
    numeroPaginas = soupAux.find('ul',class_='page-numbers').find_all('li')[-2].text
    return int(numeroPaginas)

def extraer_licores():
    nPaginas=numero_paginas()
    #nPaginas = 1
    licores_marianomadrueno=[]
    file = open("licoreslog.txt", "w",encoding="utf-8")
    for i in range(1,nPaginas+1):
        
        soup=BeautifulSoup(abrir_url( 'https://marianomadrueno.es/tienda/page/'+str(i) ),'html.parser')
        
        for licor in soup.find_all("a",class_="woocommerce-LoopProduct-link woocommerce-loop-product__link"):
            
            licorUrl=licor['href']
            
            licorSoup=BeautifulSoup(abrir_url(licorUrl),'lxml')
            
            try:
                titulo = licorSoup.find_all('h1',class_='product_title entry-title')[0].text
            except:
                titulo = None
                
            file.write(titulo+ "-Mariano Madrueno-Pagina: " + str(i) + "\n")
            try:
                precio = float(licorSoup.find_all('p',class_='price')[0].span.text.split('€')[0].replace(',','.'))
            except:
                precio = None
            referencia = None
            origen= None
    
            meta=licorSoup.find_all('div',class_='product_meta')[0].text.split(':')
            
            palabraAnterior=""
            categoriaArray=[]
            categoria = "OTROS LICORES"
            for palabra in meta:
                if("Referencia" in palabraAnterior):
                    referencia = palabra.strip()
                if("Procedencia" in palabraAnterior):
                    origen = palabra.strip().replace('Referencia','')
                if("Categoría" in palabraAnterior):
                    categoriaArray=palabra.upper().split('\n')[0].split(',')
                    for index in range(0,len(categoriaArray)):
                        categoriaArray[index] = categoriaArray[index].strip()
                palabraAnterior = palabra
            if len(categoriaArray) == 0:
                categoriaArray.append(categoria)
                
                
            urlImagen = licorSoup.find_all('img',class_='wp-post-image')[0]['src']
            
            descripcionArray = licorSoup.find_all('div',class_='woocommerce-Tabs-panel woocommerce-Tabs-panel--description panel entry-content wc-tab')
            if(len(descripcionArray)>0):
                descripcionArray = descripcionArray[0].find_all('p')#,{'style': re.compile(r'text-align*')})
            descripcion=""
            for p in descripcionArray:
                descripcion=descripcion+'\n'+p.text.strip()
                        
            graduacion=None
            
            if("%" in descripcion and "GRAD" in descripcion.upper()):
                graduacion=descripcion.split("%")[-2].split(" ")[-1]
                
                if ( not graduacion.strip().isdigit() ):
                    graduacion=None
                else:
                    graduacion=float(graduacion)
                    
            enStock = True
            stock=licorSoup.find_all('p',class_='stock in-stock')
                       
            if (len(stock)!=0):
                stock=int(stock[0].text.strip().split(' ')[0])
            else:
                stock=0
                
            if (stock<=0):
                enStock=False
            try:
                peso = licorSoup.find_all('td',class_='product_weight')[0].text.strip()
            except:
                peso = None
            diccionarioLicor = {"codigoReferencia":referencia,"titulo":titulo,"descripcion":descripcion,"precio":precio,"origen":origen,"categoria":categoriaArray,"cantidad":peso,"graduacion":graduacion,"urlProducto":licorUrl,"enStock":enStock,"urlImagen":urlImagen}
            print(diccionarioLicor)
            licores_marianomadrueno.append(diccionarioLicor)
            time.sleep(1)
    file.close()
    return licores_marianomadrueno
        
        
