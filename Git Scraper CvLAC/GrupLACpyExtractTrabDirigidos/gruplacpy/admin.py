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
        self.capLibro=[]
        
        
    
    
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
            

            if nombreSec != None and nombreSec == "Trabajos dirigidos/turorías":
                self.ProcesaSecCapDeLibro(sec, nombreGrupo)

    def ProcesaSecCapDeLibro(self, sec,nombreGrupo):
        """
        Procesa la sección de Trabajos dirigidos/turorías
        """
        print("Se logró acceder a la sección de Trabajos dirigidos/turorías")
        # Contenedor con la información de Trabajos dirigido/turoría
        contInfo = sec.findAll("tr")

        articulos=[]
        for i in range(1, len(contInfo)):
            tipo = ""
            info_articulo = contInfo[i].text
            
            #Nombre Libro
            linesInfo = [ l.strip() for l in info_articulo.split("\n")]
            linesInfo = [ l for l in linesInfo if len(l)>0]
            #print(linesInfo)
            NombreProducto=linesInfo[0]
            tipo, NombreProducto = NombreProducto.split(": ",1)
            
            tipo = tipo.split(".-",1)[1]

            #Coautores
            tutores = linesInfo[-1]
            tutores = tutores[22:]
            
            
            #Lugar

            institucion = [ l for l in linesInfo if "Institución:" in l]
            institucion = institucion[0]
            institucion = institucion[12:]
            

            #Estudiante orientado
            try:
                estudiante = linesInfo[linesInfo.index("Nombre del estudiante:")+1]
                estudiante = estudiante[0:-1]
            except:
                estudiante = ""

            #Programa académico
            programa = [ l for l in linesInfo if "Programa académico:" in l]
            programa = programa[0]
            programa = programa[programa.index(":")+1:]

            #Tipo de orientación
            tipoOrientacion = [ l for l in linesInfo if "Tipo de orientación:" in l]
            tipoOrientacion = tipoOrientacion[0]

            try:
                tipoOrientacion = tipoOrientacion[tipoOrientacion.index(":")+1:]
            except:
                tipoOrientacion = ""



            #DOI
            doi = [ l for l in linesInfo if "DOI:" in l]
            if len(doi)==0:
                doi = ""

            
            #Año
            AnoEvento = linesInfo[2]

            try:
                AnoEvento = AnoEvento[:AnoEvento.index(",")]
                AnoEvento = AnoEvento[-5:]
            except:
                AnoEvento = ""

            #Volumen
            Valoracion = [ l for l in linesInfo if "Valoración:" in l]
            Valoracion = Valoracion[0]

            try:
                Valoracion = Valoracion[Valoracion.index("n:")+2:-1]
            except:
                Valoracion = ""

            #Páginas

            numPags = [ l for l in linesInfo if "Número de páginas:" in l]
            numPags = numPags[0]

            try:
                numPags = numPags[numPags.index(":")+1:numPags.index(",")]
            except:
                numPags = ""


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
            
            capLibro = [nombreGrupo, NombreProducto, tipo, tutores,institucion, estudiante, programa, tipoOrientacion, doi,
                 AnoEvento, Valoracion, numPags,Palabras,Area,Sectores]
            self.capLibro.append(capLibro)
        
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    def SaveTrabDirigidos(self,fname):
        """
        Guarda los libros en un archivo csv
        """
        encabezado=["Grupo","Nombre del producto", "Tipo", "Tutor(es)/Cotutor(es)", "Institución",
        "Estudiante orientado","Programa académico","Tipo de orientación" , "DOI",  "Año", "Valoración","Número de Páginas", "Palabras","Area","Sectores"]
        datos=[encabezado]+self.capLibro
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
