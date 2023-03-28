"""
Administra la lectura de datos, y el modo de guardarlos
"""
from .utils import getCvlacsDirs
import bs4
import ssl
from urllib.request import urlopen
from bs4 import BeautifulSoup 
import csv
import re
# Ajusta los certificados utilizados para realizar las conexiones
ssl._create_default_https_context = ssl._create_unverified_context

class Admin(object):
    
    
    def __init__(self,filename):
        
        self.cvlacDirs=getCvlacsDirs(filename)
        self.articulos=[]
        
        
    
    
    def Run(self):
        """
        Realiza la lectura
        """
        if len(self.cvlacDirs)<2:
            print("No hay información para procesar")
            return
        for i in range(1,len(self.cvlacDirs)):
            self.LecturaCvlac(self.cvlacDirs[i][-1])

    def LecturaCvlac(self, urlCvlac):
        """
        Realiza la lectura de una url de CvLAC
        """
        uClient = urlopen(urlCvlac)
        page_html = uClient.read()
        uClient.close()
        page_soup = BeautifulSoup(page_html,"html.parser")
        # Cada sección de información se maneja como una tabla
        secciones = page_soup.findAll("table")
        nombreInvestigador = ""
        for i, sec in enumerate( secciones[0:] ):
            nombreSec = sec.h3
            if nombreSec != None:
                nombreSec = nombreSec.text
            else:
                nombreSec = ""
            if nombreSec != "":
                print(f"seccion {i}:", nombreSec)
            # Extrae el nombre del investigador
            if nombreInvestigador == "" and nombreSec == "" :
                tdNombre = self.ExtraerTag(sec,['tr','td'])
                
                filas = sec.findAll("tr", limit=12)
                for fila in filas:
                    if fila.td.text == "Nombre":
                        nombreInvestigador = fila.findAll("td")[1].text.strip()
                        print("  Nombre identificado:", nombreInvestigador)
                        break

            elif nombreSec != None and nombreSec == "Artículos":
                self.ProcesaSecArticulos(sec, nombreInvestigador)

    def ProcesaSecArticulos(self, sec,investigador):
        """
        Procesa la sección de artículos
        """
        # Contenedor con la información de cada artículo
        contInfo = sec.findAll("blockquote")
        # contenedor con los títulos con el tipo del artículo
        contTipo = sec.findAll("li") 
        
        articulos=[]
        for i in range(0, len(contInfo)):
            tipo = contTipo[i].text
            info_articulo = contInfo[i].text
            
            #Nombre Articulo
            linesInfo = [ l.strip() for l in info_articulo.split("\n")]
            linesInfo = [ l for l in linesInfo if len(l)>0]
            NombreProducto=""
            listaAutores=[]
            lineaClave=-1
            for i, l in enumerate(linesInfo):
                if l[-1]==',':
                    listaAutores.append(l[:-1])
                if  l[0] == '"':
                    NombreProducto = l[1:-1]
                    lineaClave = i
                    break
            
            #NombreProducto = info_articulo[index1:index2]
            #print(linesInfo)
            #for l in linesInfo:
            #    print(l)
            #print("Nombre Producto", NombreProducto)
            #Tipo Artículo
            if tipo.strip() == "Producción bibliográfica - Artículo - Publicado en revista especializada":
                tipo = "Artículo - Publicado en revista especializada"
            elif tipo.strip() == "Producción bibliográfica - Artículo - Corto (Resumen)":
                tipo = "Artículo - Corto (Resumen)"
            elif tipo.strip() == "Producción bibliográfica - Artículo - Revisión (Survey)":
                tipo = "Artículo - Revisión (Survey)"
            elif tipo.strip() == "Producción bibliográfica - Artículo - Caso clínico":
                tipo = "Artículo - Caso clínico"
            else:
                print ("ALERTA: tipo de artículo no reconocido")
            #Coautores
            coautores = ", ".join(listaAutores)
            #Lugar

            lugar = linesInfo[lineaClave+1]
            lugar = lugar[4:]
            lugar = lugar.replace(":"," ")
            #Editorial
            editorial = linesInfo[lineaClave+4]
            editorial = editorial.replace("\xa0"," ")
            editorial = editorial[3:]
            #DOI
            doi = linesInfo[lineaClave+10]
            doi = doi.replace("\xa0"," ")
            doi = doi[4:]
            #ISSN
            ISSN = linesInfo[lineaClave+3]
            ISSN = ISSN.replace("\xa0"," ")
            ISSN = ISSN[5:]
            #Nombre Revista
            Revista = linesInfo[lineaClave+2]
            #Año
            AnoEvento = linesInfo[lineaClave+9]
            AnoEvento = AnoEvento[1:-1]
            #Volumen
            Volumen = linesInfo[lineaClave+5]
            Volumen = Volumen.replace("."," ")
            Volumen = Volumen[1:]
            #Fasciculo
            fasciculo = linesInfo[lineaClave+6]
            fasciculo = fasciculo.replace("."," ")
            fasciculo = fasciculo[4:]
            #Páginas

            Pagini = linesInfo[lineaClave+7]
            Pagini = Pagini.replace("."," ")
            Pagini = Pagini[1:]

            Pagfin = linesInfo[lineaClave+8]
            Pagfin = Pagfin.replace("-"," ")
            Pagfin = Pagfin[1:]

            #Palabras
            try:
                Palabras = linesInfo[linesInfo.index("Palabras:")+1]
            except:
                Palabras = ""
            #Area
            try:
                Area = linesInfo[linesInfo.index("Areas:")+1]
            except:
                Area = ""
            #Sectores
            try:
                Sectores = linesInfo[linesInfo.index("Sectores:")+1]
            except:
                Sectores = ""
            
            articulo = [investigador, NombreProducto, tipo, coautores,lugar, editorial, doi,
                ISSN, Revista, AnoEvento, Volumen, fasciculo, Pagini,Pagfin,Palabras,Area,Sectores]
            self.articulos.append(articulo)
        
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    def SaveArticulos(self,fname):
        """
        Guarda los articulos en un archivo csv
        """
        encabezado=["Investigador","Nombre del producto", "Tipo", "Autores", "Lugar",
        "Editorial", "DOI", "ISSN", "Revista","Año", "Volumen","Fasciculo",
        "Página inicial","Página final","Palabras","Area","Sectores"]
        datos=[encabezado]+self.articulos
        with open( fname,'w', encoding="UTF-8") as f:
            writer = csv.writer(f, delimiter=',',quotechar='"')
            for row in datos:
                writer.writerow(row)
    
    
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    def ExtraerTag(self,soup,ruta):
        """
        Extrae un un tag siguiendo la ruta de nodos en orden descendente, si 
        reverse está activado la ruta indica como ascender en el arbol
        """
        tagResultado = soup
        for tagName in ruta:
            tagResultado = tagResultado.find(tagName)
            #print("  tag:",tagName)
            if tagResultado == None:
                break
        return tagResultado
