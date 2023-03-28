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
            

            if nombreSec != None and nombreSec == "Capítulos de libro publicados ":
                self.ProcesaSecCapDeLibro(sec, nombreGrupo)

    def ProcesaSecCapDeLibro(self, sec,nombreGrupo):
        """
        Procesa la sección de capítulos de libro
        """
        print("Se logró acceder a la sección de capítulos de libro publicados")
        # Contenedor con la información de CapDeLibro
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

            #Coautores
            coautores = linesInfo[-1]
            coautores = coautores[8:]
            
            otherInfo = linesInfo[1].split(",")
            
            #Lugar

            lugar = otherInfo[0]
            

            #Editorial
            editorial = otherInfo[-1]
            editorial = editorial[4:]

            #Libro
            libro =otherInfo[2]

            #DOI
            doi = [ l for l in linesInfo if "DOI:" in l]
            if len(doi)==0:
                doi = ""

            #ISBN
            ISBN = [ l for l in otherInfo if "ISBN" in l]
            ISBN = ISBN[0]

            try:
                ISBN = ISBN[ISBN.index("ISBN")+5:]
            except:
                ISBN = ""

            
            #Año
            AnoEvento = otherInfo[1]

            #Volumen
            Volumen = [ l for l in otherInfo if "Vol." in l]
            Volumen = Volumen[0]
            Volumen = Volumen[4:]

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
            
            capLibro = [nombreGrupo, NombreProducto, tipo, coautores,lugar, editorial, libro, doi,
                ISBN, AnoEvento, Volumen, Pagini, Pagfin ,Palabras,Area,Sectores]
            self.capLibro.append(capLibro)
        
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    def SaveCapDeLibro(self,fname):
        """
        Guarda los libros en un archivo csv
        """
        encabezado=["Grupo","Nombre del producto", "Tipo", "Autores", "Lugar",
        "Editorial","Libro" , "DOI", "ISBN", "Año", "Volumen","Página inicial", "Página final", "Palabras","Area","Sectores"]
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
