import os

import urllib.request

from bs4 import BeautifulSoup
import time

dirdocs="licores"
dirindex="Index"

def abrir_url(url):
    r = urllib.request.urlopen(url)
    return r

def numero_paginas(url):
    soupAux = BeautifulSoup(abrir_url(url),'html.parser')
    numeroPaginas = soupAux.find('ul',class_='pagination').find_all('li')[-2].text
    return int(numeroPaginas)

def extraer_texto_disevil():
    if not os.path.exists(dirindex):
        os.mkdir(dirindex)
    nPaginas = numero_paginas('https://www.disevil.com/tienda/es/80-licores-y-destilados/')
    #nPaginas = 1
    categorias = ['AGUARDIENTE','ABSENTA','BRANDY','COGNAC','ARMAGNAC','WHYSKY','BOURBON','GINEBRA','RON','VODKA','TEQUILA']
    licores_disevil=[]
    file = open("licoreslog.txt", "a",encoding="utf-8")
    for i in range(1,20+1):#paginas+1):
        soup=BeautifulSoup(abrir_url('https://www.disevil.com/tienda/es/80-licores-y-destilados/?p='+str(i)+"/"),'html.parser')
        
        
        for enlace in soup.find_all(class_='quick-view'):
    
            url = enlace['href']

            soup2 = BeautifulSoup(abrir_url(url),'html.parser')
            
            try:
                producto = soup2.find(itemtype="http://schema.org/Product")
            except:
                producto = None
            titulo = " " + producto.find(itemprop="name").text + " "
            
            
            file.write(titulo+ "-Disevil-Pagina: " + str(i) + "\n")
            
            try:
                descripcion1 = producto.find(itemprop="description")
            except:
                descripcion1 = None
                
            if(descripcion1 !=None):
                descripcion1 = descripcion1.text
            else:
                descripcion1=""
            
            try:
                precio= float(producto.find(itemprop="price").text.replace(",",".").replace("€",""))
            except:
                precio = None
                
            try:
                referencia= producto.find(itemprop="sku").text
            except:
                referencia = None
            enlace=url
            
            try:
                urlImagen=producto.find(itemprop="image")['src']
            except:
                urlImagen = None
                
            try:
                urlStock = producto.find(itemprop="availability")
            except:
                urlStock = None
            if urlStock != None:
                urlStock = urlStock['href']
                
            enStock = True
            
            if(urlStock != 'http://schema.org/InStock'):
                enStock= False
                
            categoria = None
            for cat in categorias:
                if cat in titulo:
                    categoria=cat
                    break
            if(categoria== None):
                if 'GIN' in titulo:
                    categoria = 'GINEBRA'
                else:
                    categoria='OTROS LICORES'        
            categoria=[categoria]
            try:
                descripcion2 = producto.find(class_='page-product-box').text
            except:
                descripcion2 = None
            
            try:
                if "Bot" in descripcion2:
                   
                    volumen =  descripcion2.split('Bot')[1]
                    volumen = volumen.replace(" ","")
                    volumen = volumen.replace(".","")
                
                    volumen = volumen.upper()
            
                    volumen = volumen.split("º")[0]
                    volumen = volumen.replace("CL", "CLKKK")
                    volumen = volumen.replace("1L","1LKKK")
                    volumen = volumen.split("KKK")[0]
               
                    if volumen.strip() == "0":
                        volumen = "70CL"
                    
                        
                    else:
                        volumen = None
                    volumen = volumen.replace(" ","")
                    volumen = volumen.replace("070","70")
            except:
                    volumen = None
                    
            try:
                if "Bot" in descripcion2:
                    graduacion= descripcion2.split('Bot')[1]
                    graduacion = graduacion.upper()
                    graduacion = graduacion.replace("º","ºKKK")
                    graduacion = graduacion.replace("CL","CL.")
                    graduacion = graduacion.replace("CL..","CL.")
                    graduacion = graduacion.replace(" ","")
                    graduacion = graduacion.replace("L","L.")
                    graduacion = graduacion.replace("L..","L.")
                    graduacion = graduacion.split("KKK")[0]
                    graduacion = graduacion.split("L")[1]
                    graduacion = graduacion.split(".")[1]
                    graduacion = graduacion.replace(" ","")
                    if("º" not in graduacion):
                        graduacion = str(graduacion) +"º"
                    try:
                        graduacion = float(graduacion.replace(" ","").replace("º",""))
                    except:
                        graduacion = None
                        
                else:
                    graduacion = None
            except:
                graduacion = None
            try:
                origen= descripcion2.splitlines()[1]
                if "Más" in origen:
                    origen = descripcion2.splitlines()[2]
                    origen = origen.split("Origen")[1]
                    origen = origen.replace(":","")
                
                if origen == "":
                    origen = None
                
                origen = origen.replace(" ","")
                origen = origen.replace(".","")
                if len(origen) > 30:
                    origen = None
            except:
                origen = None
            
        
            descripcion = descripcion1 + descripcion2
            diccionarioLicor = {"codigoReferencia":referencia,"titulo":titulo,"descripcion":descripcion,"precio":precio,"origen":origen,"categoria":categoria,"cantidad":volumen,"graduacion":graduacion,"urlProducto":url,"enStock":enStock,"urlImagen":urlImagen}
            print(diccionarioLicor)
            licores_disevil.append(diccionarioLicor)
            time.sleep(1)
    file.close()
            
    return licores_disevil
    
    