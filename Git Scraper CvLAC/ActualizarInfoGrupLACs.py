# El programa CvLACpyExtractArticulos fue creado por Carlos Antonio Jacanamejoy Jamioy y
# sus modificaciones y derivados CvLACpyExtract(tipo de producto) fueron creados por
# Camilo Eduardo Echeverry Naranjo con fines de Acreditación y para uso exclusivo de la
# Universidad de Ibagué. Reservados todos los derechos por la Universidad de Ibagué.

import os
import subprocess
import shutil

#Proceso de extracción de información
#--------------------------------------------------------------------------------------------------------------

#Extrae Información de artículos
os.chdir('GrupLACpyExtractArticulos')
subprocess.call("python main.py", shell=True)
os.chdir("..")

try:
    shutil.copy2('GrupLACpyExtractArticulos/Output/articulos.csv','GrupLACResults/articulos.csv')
    print('articulos copiados con éxito')
except:
    print('No se pudo copiar el archivo articulos.csv')

#Extrae Información de capítulos de libro
os.chdir('GrupLACpyExtractCapDeLibros')
subprocess.call("python main.py", shell=True)
os.chdir("..")

try:
    shutil.copy2('GrupLACpyExtractCapDeLibros/Output/Capitulos_de_libro.csv','GrupLACResults/Capitulos_de_libro.csv')
    print('Capitulos_de_libro copiados con éxito')
except:
    print('No se pudo copiar el archivo Capitulos_de_libro.csv')


#Extrae Información de Eventos
os.chdir('GrupLACpyExtractEventos')
subprocess.call("python main.py", shell=True)
os.chdir("..")

try:
    shutil.copy2('GrupLACpyExtractEventos/Output/Eventos.csv','GrupLACResults/Eventos.csv')
    print('Eventos copiados con éxito')
except:
    print('No se pudo copiar el archivo Eventos.csv')

#Extrae Información de Integrantes
os.chdir('GrupLACpyExtractIntegrantes')
subprocess.call("python main.py", shell=True)
os.chdir("..")

try:
    shutil.copy2('GrupLACpyExtractIntegrantes/Output/Integrantes.csv','GrupLACResults/Integrantes.csv')
    print('Integrantes copiados con éxito')
except:
    print('No se pudo copiar el archivo Integrantes.csv')


#Extrae Información de Libros
os.chdir('GrupLACpyExtractLibros')
subprocess.call("python main.py", shell=True)
os.chdir("..")

try:
    shutil.copy2('GrupLACpyExtractLibros/Output/libros.csv','GrupLACResults/libros.csv')
    print('libros copiados con éxito')
except:
    print('No se pudo copiar el archivo libros.csv')



#Extrae Información de Proyectos
os.chdir('GrupLACpyExtractProyectos')
subprocess.call("python main.py", shell=True)
os.chdir("..")

try:
    shutil.copy2('GrupLACpyExtractProyectos/Output/Proyectos.csv','GrupLACResults/Proyectos.csv')
    print('Proyectos copiados con éxito')
except:
    print('No se pudo copiar el archivo Proyectos.csv')


#Extrae Información de Trabajos Dirigidos
os.chdir('GrupLACpyExtractTrabDirigidos')
subprocess.call("python main.py", shell=True)
os.chdir("..")

try:
    shutil.copy2('GrupLACpyExtractTrabDirigidos/Output/Trabajos_dirigidos.csv','GrupLACResults/Trabajos_dirigidos.csv')
    print('Trabajos_de_Grado copiados con éxito')
except:
    print('No se pudo copiar el archivo Trabajos_de_Grado.csv')

