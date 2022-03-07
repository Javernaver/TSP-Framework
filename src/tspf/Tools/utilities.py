"""
Modulo con las utilidades utilizadas por los demas modulos

"""

import random
import csv
from os import path
from pathlib import Path

# Numero maximo de archivos de salida para ser reemplazados
NUM_FILES = 30

class bcolors:
    """ Clase cuyo objetivo es cambiar de color los output por consola """
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKCYAN = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''
        self.BOLD = ''
        self.UNDERLINE = ''


class Trajectory():
    """ Clase cuyo fin es almacenar datos de la trayectoria recorrida por las soluciones de los algorimtos

        Parameters
        ----------
        tour : list
            lista con el recorrido
        cost : int
            calidad del recorrido
        iterations : int
            numero de iteraciones al llegar a la solución
        evaluations : int
            numero de evaluaciones al llegar a la solución
        average : float, optional
            promedio de las soluciones de la población (Algoritmo Genetico)
        deviation : float, optional
            deviacion estandar de las soluciones de la población (Algoritmo Genetico)
        temperature : float, optional
            temperatura al momemto de la solución (simulated annealing)

        Examples
        --------
        >>> tra = Trajectory([0,1,2,3,4,5,6,7,8,9,0],
                            3542, 10, 15,
                            temperature=950.31)
    """
    def __init__(self, tour: list, cost: int, iterations: int,
                 evaluations: int, average: float = 0.0, deviation: float = 0.0,
                 temperature: float = -1.0, worst: int = -1) -> None:
        self.tour = tour
        self.cost = cost
        self.iterations = iterations
        self.evaluations = evaluations
        self.worst = worst # peor costo de la población (algoritmo genetico)
        self.average = average # promedio de la población (algoritmo genetico)
        self.deviation = deviation # desviacion estandar (algoritmo genetico)
        self.temperature = temperature # temperatura (simulated annealing)



def dtrunc (x: float) -> float:
    """ Truncar un numero float """

    k = int(x)
    x = float(k) # numero float sin parte decimal
    return x



def printSolToFile(outputFile: str, tour: list) -> None:
    """ Guardar la solución para una instacia y ejecución en un archivo recibido por parámetro """
    if not outputFile or not tour:
        return
    try:
        # crea la carpeta output si es que no existe y se usa la salida por defecto
        Path("output/").mkdir(exist_ok=True)
        print(f"{bcolors.OKGREEN}\nGuardando solución en archivo... {bcolors.ENDC}{path.abspath(outputFile)}")
        # Comprobar si existe el archivo y renombrar si es el caso
        outputFile = checkFile(outputFile)

        # Abrir archivo para escribir o reemplazar
        file = open(outputFile, 'w')

        # crear texto con la solución separando cada elemento con espacios y luego guardarlo en el archivo
        sol = " ".join([str(elem) for elem in tour])
        file.write(sol)
        file.close()
    except IOError:
        print(f"{bcolors.FAIL}No se pudo guardar el archivo... {outputFile} Error: {IOError}{bcolors.ENDC}")
        print(f"{bcolors.FAIL}Asegurese de tener permisos de escritura en la ruta y que esta bien escrita{bcolors.ENDC}")



def printTraToFile(trajectoryFile: str, trajectory: list) -> None:
    """ Guardar la trayectoria de una solución para una instacia y ejecución en un archivo recibido por parámetro """
    if not trajectoryFile or not trajectory:
        return
    try:
        # crea la carpeta output si es que no existe y se usa la salida por defecto
        Path("output/").mkdir(exist_ok=True)
        print(f"{bcolors.OKGREEN}\nGuardando trayectoria de la solución en archivo... {bcolors.ENDC}{path.abspath(trajectoryFile)}")
        # Comprobar si existe el archivo y renombrar si es el caso
        trajectoryFile = checkFile(trajectoryFile)

        # Abrir archivo para escribir o reemplazar
        csvfile = open(trajectoryFile, 'w', newline="\n")

        # Headers
        fields = ["Iterations","Evaluations","cost","solution"]
        writer = csv.DictWriter(csvfile, delimiter=';', fieldnames=fields)
        writer.writeheader()
        # crear texto con la solución separando cada elemento con espacios y luego guardarlo en el archivo
        for tra in trajectory:
            sol = " ".join([str(elem) for elem in tra.tour])
            # escribir la mejor solución y todas las caracteristicas de su ejecución
            writer.writerow({
                "Iterations": tra.iterations, 
                "Evaluations": tra.evaluations,
                "cost": tra.cost, 
                "solution": sol
            })

        csvfile.close()
    except IOError:
        print(f"{bcolors.FAIL}No se pudo guardar el archivo... {trajectoryFile} Error: {IOError}{bcolors.ENDC}")
        print(f"{bcolors.FAIL}Asegurese de tener permisos de escritura en la ruta y que esta bien escrita{bcolors.ENDC}")



def checkFile(filePath: str) -> str:
    """Comprueba si el archivo existe en la ruta recibida y si existe renombra el archivo de salida"""

    if path.exists(filePath):

        #print(f"{bcolors.WARNING}Advertencia: Ya existe el archivo{bcolors.ENDC} {path.abspath(filePath)}")
        print(f"{bcolors.WARNING}Advertencia: Ya existe el archivo{bcolors.ENDC}")
        
        num = 1
        name = path.splitext(filePath) # Separe el nombre del archivo de la extension
        files = [] # lista con las rutas para utilizar en el límite
        files.append(filePath)
        
        while True:
            # Limite de archivos para evitar llenar de exceso de archivos
            if num > NUM_FILES:
                # obtener archivo mas antiguo de las rutas
                old = min(files, key=lambda pth: path.getmtime(pth))
                #print(old)
                print(f"{bcolors.FAIL}Se ha superado el límite de archivos con el mismo nombre, se reemplazará el más viejo {bcolors.ENDC}")
                print(f"{bcolors.FAIL}Guardando en... {bcolors.ENDC} {path.abspath(old)}")
                return old
            
            newPath = f"{name[0]}_{num}{name[1]}"
            files.append(newPath)
            if path.exists(newPath):
                num += 1
            else:
                print(f"{bcolors.FAIL}Se guardará en{bcolors.ENDC} {path.abspath(newPath)}")
                return newPath

    return filePath