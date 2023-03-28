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
        self.libro=[]
        
        
    
    
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
            

            if nombreSec != None and nombreSec == "Proyectos":
                self.ProcesaSecProyectos(sec, nombreGrupo)

    def ProcesaSecProyectos(self, sec,nombreGrupo):
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
            
            #Nombre Libro
            linesInfo = [ l.strip() for l in info_articulo.split("\n")]
            linesInfo = [ l for l in linesInfo if len(l)>0]
            print(linesInfo)
            NombreProducto=linesInfo[0]
            tipo, NombreProducto = NombreProducto.split(": ",1)
            
            tipo = tipo.split(".-",1)[1]
            
            print(tipo)
            
            #Años
            if tipo==" Extensión y responsabilidad social CTI":
                AnoInicio = ""
                AnoFin = ""
            else:
                AnoInicio = linesInfo[1]
                AnoInicio = AnoInicio[:-2]
                AnoFin = linesInfo[2]
            
            
            

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
            
            libro = [nombreGrupo, NombreProducto, tipo, AnoInicio,AnoFin]
            self.libro.append(libro)
        
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    def SaveProyectos(self,fname):
        """
        Guarda los libros en un archivo csv
        """
        encabezado=["Grupo","Nombre del producto", "Tipo", "Año inicio","Año fin"]
        datos=[encabezado]+self.libro
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
