import os

import urllib.request
import time
from bs4 import BeautifulSoup

dirdocs="licores"
dirindex="Index"

def abrir_url(url):
    r = urllib.request.urlopen(url)
    return r

def numero_paginas(url):
    soupAux = BeautifulSoup(abrir_url(url),'html.parser')
    numeroPaginas = soupAux.find(class_='page-numbers').find_all('li')[-2].text
    return int(numeroPaginas)

def extraer_texto_casalicores():
    if not os.path.exists(dirindex):
        os.mkdir(dirindex)
    
    nPaginas = numero_paginas('http://lacasadeloslicores.es/tienda/')
    #nPaginas = 20
    licores_casalicores=[]
    file = open("licoreslog.txt", "a",encoding="utf-8")
    
    for i in range(1,nPaginas+1):#paginas+1):
        try:
            soup=BeautifulSoup(abrir_url('http://lacasadeloslicores.es/tienda/page/'+str(i)+"/"),'html.parser')
            
            for enlace in soup.find_all('div',class_='archive-products')[0].find_all('li'):
                
                urlImagen = enlace.find(class_= "inner").img['src']
                url = enlace.find(class_="product-image").a['href']
                
                soup2 = BeautifulSoup(abrir_url(url),'html.parser')
                
                producto = soup2.find(itemtype = 'http://schema.org/Product')
                
                try:
                    titulo = producto.find(itemprop='name').text
                except:
                    titulo = None
                
                file.write(titulo+ "-Casa Licores-Pagina: " + str(i) + "\n")
                
                try:
                    descripcionEntera = producto.find(class_="resp-tabs-container")
                except:
                    descripcionEntera = None
                try:
                    descripcion = descripcionEntera.text.split("Reseñas")[0].strip()
                    descripcion = descripcion.split('CATA')[0].strip()
                    descripcion = descripcion.split('Tipo')[0].strip()
                except:
                    descripcion = None
                
                try:
                    producto2 = soup2.find(class_="product-summary-wrap")
                except:
                    producto2= None
                try:
                    referencia = producto2.find(class_="sku").text
                except:
                    referencia = None
                try:
                    precio = producto2.find(class_="price").text
                    precio = float(precio.replace(",",".").replace("€",""))
                except:
                    precio = None
                    
                try:
                    urlStock = producto.find(itemprop="availability")
                except:
                    urlStock = None
                    
                if urlStock != None:
                    urlStock = urlStock['href']
                    
                enStock = True
                
                if(urlStock != 'http://schema.org/InStock'):
                    enStock= False
                
                try:
                    categoria = producto2.find(class_="posted_in").text.split('Categoría:')[1].strip()
                except:
                    categoria = "OTROS LICORES"
                
                try:
                    volumen = producto.find(class_="goog-text-highlight")[0].text
                    
                except:
                    volumen = None
                
                try:
                    graduacion = float(producto.find(class_="goog-text-highlight")[1].text.replace("º",""))
                    
                except:
                    graduacion = None
                    
             
                #tupla = (referencia,titulo,descripcion,precio,categoria,volumen,graduacion,url,enStock,urlImagen)
                categoria=[categoria]
                diccionarioLicor = {"codigoReferencia":referencia,"titulo":titulo,"descripcion":descripcion,"precio":precio,"origen":"Desconocido","categoria":categoria,"cantidad":volumen,"graduacion":graduacion,"urlProducto":url,"enStock":enStock,"urlImagen":urlImagen}
                print(diccionarioLicor)
                licores_casalicores.append(diccionarioLicor)
                time.sleep(1)
        except:
            continue
    file.close()
    return licores_casalicores
    
    