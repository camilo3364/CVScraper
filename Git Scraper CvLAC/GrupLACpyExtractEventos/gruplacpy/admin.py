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
        self.evento=[]
        
        
    
    
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
            

            if nombreSec != None and nombreSec == "Eventos Científicos":
                self.ProcesaSecCapDeLibro(sec, nombreGrupo)

    def ProcesaSecCapDeLibro(self, sec,nombreGrupo):
        """
        Procesa la sección de Eventos Científicos
        """
        print("Se logró acceder a la sección de Eventos Científicos")
        # Contenedor con la información de Eventos Científicos
        contInfo = sec.findAll("tr")

        articulos=[]
        for i in range(1, len(contInfo)):
            tipo = ""
            info_evento = contInfo[i].text
            
            #Nombre Libro
            linesInfo = [ l.strip() for l in info_evento.split("\n")]
            linesInfo = [ l for l in linesInfo if len(l)>0]
            #print(linesInfo)
            NombreProducto=linesInfo[0]
            tipo, NombreProducto = NombreProducto.split(": ",1)
            
            tipo = tipo.split(".-",1)[1]

            #Coautores
            tutores = linesInfo[-1]
            tutores = tutores[22:]
            
            
            #Lugar
            lugar = linesInfo[1]
            lugar = lugar.split(", desde",1)[0]

            #Instituciones asociadas
            institucion = [ l for l in linesInfo if "Nombre de la institución:" in l]
            if len(institucion)==0:
                institucion = ""
            else:
                institucion = institucion[0]
                institucion = institucion[institucion.index(":")+1:]
            

            #Participación
            try:
                participacion = [ l for l in linesInfo if "Tipos de participación:" in l]
                participacion = participacion[0].split(",",1)[1]
                participacion = participacion[24:]
            except:
                participacion = ""

            #Ámbito
            ambito = [ l for l in linesInfo if "Ámbito:" in l]
            ambito = ambito[0]
            ambito = ambito[ambito.index(":")+1:ambito.index(",")]

            
            
            #Año
            AnoEvento = linesInfo[1]
            AnoEvento = AnoEvento.split(", desde",1)[1]
            AnoEvento = AnoEvento[:-1]

            AnoEvento, MesEvento, DiaEvento = AnoEvento.split("-")

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
            
            evento = [nombreGrupo, NombreProducto, tipo, lugar,institucion, participacion, ambito, 
                 AnoEvento,MesEvento, DiaEvento, Palabras,Area,Sectores]
            self.evento.append(evento)
        
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    def SaveEventos(self,fname):
        """
        Guarda los libros en un archivo csv
        """
        encabezado=["Grupo","Nombre del Evento", "Tipo", "Lugar", "Institución",
        "Participación","Ámbito",  "Año","Mes","Día", "Palabras","Area","Sectores"]
        datos=[encabezado]+self.evento
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
