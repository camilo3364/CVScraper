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
        self.integrante=[]
        
        
    
    
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
            

            if nombreSec != None and nombreSec == "Integrantes del grupo":
                self.ProcesaSecIntegrantes(sec, nombreGrupo)

    def ProcesaSecIntegrantes(self, sec,nombreGrupo):
        """
        Procesa la sección de Integrantes del grupo
        """
        print("Se logró acceder a la sección de Integrantes del grupo")
        # Contenedor con la información de cada Integrante
        contInfo = sec.findAll("tr")

        articulos=[]
        for i in range(2, len(contInfo)):
            Vinculacion = ""
            info_integrante = contInfo[i].text
            
            #Nombre Libro
            linesInfo = [ l.strip() for l in info_integrante.split("\n")]
            linesInfo = [ l for l in linesInfo if len(l)>0]
            print(linesInfo)
            NombreIntegrante=linesInfo[0]
            NombreIntegrante = NombreIntegrante.split(".- ")[1]
            
            Vinculacion = linesInfo[1]

            #HorasDe dedicacion
            HorasDedicacion = linesInfo[2]
            
            
            #Año
            fechaInicio, fechaFin = linesInfo[-1].split(" - ")

            AnoInicio, MesInicio = fechaInicio.split("/")
            if fechaFin != "Actual":
                AnoFin, MesFin = fechaFin.split("/")
            else:
                AnoFin, MesFin = "Actual", "Actual"
            
            

            
            integrante = [nombreGrupo, NombreIntegrante, Vinculacion, HorasDedicacion, AnoInicio, MesInicio,AnoFin,MesFin]
            self.integrante.append(integrante)
        
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    def SaveIntegrantes(self,fname):
        """
        Guarda los libros en un archivo csv
        """
        encabezado=["Grupo","Nombre", "Vinculación", "Horas dedicación", "Año de inicio","Mes de inicio","Año de fin", "Mes de fin"]
        datos=[encabezado]+self.integrante
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
