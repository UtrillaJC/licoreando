'''
Created on 22 ene. 2019

@author: viento
'''

from distance import levenshtein
from stop_words import get_stop_words
from unidecode import unidecode


def getPuntuacionAtributo(atributoForm,atributoLicor, puntuacionForm):
    coincidencia=getPuntuacionFrase(atributoForm,atributoLicor)
    puntuacion=0
    if(coincidencia>=1.0):
        puntuacion=puntuacionForm/10.0
    return puntuacion


def getPuntuacionFrase(fraseFormulario,fraseLicor):
    fraseFormularioF=filtrarPalabrasSinSignificado(fraseFormulario)
    fraseLicorF=filtrarPalabrasSinSignificado(fraseLicor)
    fraseLicorFDictCount=cuentaPalabras(fraseLicorF)
    
    coincidenciasTotales=0.
    numeroPalabras=0.
    for palabra in fraseFormularioF:
        numeroPalabras=numeroPalabras+1.
        coincidenciasTotales=coincidenciasTotales+getLevenshteinWordsCount(palabra,fraseLicorFDictCount)
    
    #Si en la frase del licor aparece dos veces la frase del formulario la puntuación
    #será 2.0.
    puntuacion=coincidenciasTotales/numeroPalabras
    
    return puntuacion
    


def cuentaPalabras(frase):
    palabrasContadas= {}
    for palabra in frase:
        if palabra in palabrasContadas.keys():
            palabrasContadas[palabra] = palabrasContadas[palabra]+1
        else:
            palabrasContadas[palabra] = 1
            
    return palabrasContadas


def filtrarPalabrasSinSignificado(frase):
    frase=frase.replace(".","").replace(",","").replace(";","").replace(":","").lower()
    frase=unidecode(frase)
    palabrasFiltradas = [palabra for palabra in frase.split(" ") if not palabra in get_stop_words("spanish")]
    return palabrasFiltradas

def getLevenshteinDistance(word1,word2):
    return levenshtein(word1,word2)

def getLevenshteinWordsCount(toCompare,wordsDict,distance=1):
    count = 0
    distance = round(len(toCompare)/4)
    for key, value in wordsDict.items():
        d=getLevenshteinDistance(toCompare, key)
        if(d<=distance):
            count=count+value
    return count

def getPuntuacionRango(valor,mini,maxi):
    if(mini>maxi):
        miniTemp=mini
        mini=maxi
        maxi=miniTemp
        
    mediaRango=(mini+maxi)/2.0
   
    diferenciaMediaValor=mediaRango-valor
    if(diferenciaMediaValor<0):
        diferenciaMediaValor=diferenciaMediaValor*(-1.0)
        
    diferenciaMinMax=maxi-mini
    
    #Cuanto más cercano de 0 sea diferenciaMediaValor de la media
    #más se acercará la puntuación de 1, si valor sale del rango,
    #aparecerán puntuaciones negativas.
    puntuacion=(mediaRango-(diferenciaMediaValor+mini))/diferenciaMinMax
    
    #Necesario para calibrar la puntuación cuando es positiva.
    if(puntuacion>0):
        puntuacion=puntuacion*2
        
    return puntuacion
