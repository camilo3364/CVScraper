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
        
        

        try:
            nombreGrupo = page_soup.findAll("span")
            nombreGrupo = nombreGrupo[0].text
        except:
            nombreGrupo = ""


        for i, sec in enumerate( secciones[0:] ):
            nombreSec = sec.td
            if nombreSec != None:
                nombreSec = nombreSec.text
            else:
                nombreSec = ""
            if nombreSec != "":
                print(f"seccion {i}:", nombreSec)

            # Extrae el nombre del investigador
            

            if nombreSec != None and nombreSec == "Artículos publicados":
                self.ProcesaSecArticulos(sec, nombreGrupo)

    def ProcesaSecArticulos(self, sec,nombreGrupo):
        """
        Procesa la sección de artículos
        """
        print("Se logró acceder a la sección de articulos publicados")
        # Contenedor con la información de cada artículo
        contInfo = sec.findAll("tr")

        articulos=[]
        for i in range(1, len(contInfo)):
            tipo = ""
            info_articulo = contInfo[i].text
            
            #Nombre Articulo
            linesInfo = [ l.strip() for l in info_articulo.split("\n")]
            linesInfo = [ l for l in linesInfo if len(l)>0]
            #print(linesInfo)
            NombreProducto=linesInfo[0]
            tipo, NombreProducto = NombreProducto.split(": ",1)
            
            tipo = tipo.split(".-",1)[1]

            #Coautores
            coautores = linesInfo[-1]
            coautores = coautores[8:]
            lineaClave=0
            
            otherInfo=linesInfo[1].split(",")
            #Lugar

            lugar = otherInfo[0]

            #Editorial
            editorial = otherInfo[1]
            try:
                editorial = editorial[0:editorial.index("ISSN")]
            except:
                editorial = otherInfo[1]

            #DOI
            doi = otherInfo[-1]
            doi = doi[5:]
            #ISSN
            ISSN = [ l for l in otherInfo if "ISSN" in l]
            ISSN = ''.join(ISSN)

            try:
                ISSN = ISSN[ISSN.index("ISSN")+5:]
            except:
                ISSN = ""

            #Nombre Revista
            Revista = editorial
            #Año
            AnoEvento = [ l for l in otherInfo if "vol:" in l]
            AnoEvento = ''.join(AnoEvento)
            AnoEvento = AnoEvento[:5]
            #Volumen
            Volumen = [ l for l in otherInfo if "vol:" in l]
            Volumen = Volumen[0]
            

            try:
                Volumen = Volumen[Volumen.index("vol:")+4:Volumen.index("fasc:")]
            except:
                Volumen = ""
            
            #Fasciculo
            fasciculo = [ l for l in otherInfo if "fasc:" in l]
            fasciculo = fasciculo[0]
            try:
                fasciculo = fasciculo[fasciculo.index("fasc:")+6:fasciculo.index("págs:")]
            except:
                fasciculo = ""
            #Páginas

            Pagini = [ l for l in otherInfo if "págs:" in l]
            Pagini = Pagini[0]

            try:
                Pagini = Pagini[Pagini.index("págs:"):Pagini.index("-")]
                Pagini = Pagini[5:]
            except:
                Pagini = ""


            Pagfin = [ l for l in otherInfo if "págs:" in l]
            Pagfin = Pagfin[0]

            try:
                Pagfin = Pagfin[Pagfin.index("-"):]
                Pagfin = Pagfin[1:]
            except:
                Pagfin = ""
            

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
            
            articulo = [nombreGrupo, NombreProducto, tipo, coautores,lugar, editorial, doi,
                ISSN, Revista, AnoEvento, Volumen, fasciculo, Pagini,Pagfin,Palabras,Area,Sectores]
            self.articulos.append(articulo)
        
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    def SaveArticulos(self,fname):
        """
        Guarda los articulos en un archivo csv
        """
        encabezado=["Grupo","Nombre del producto", "Tipo", "Autores", "Lugar",
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
