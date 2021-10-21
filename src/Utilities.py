import random
import sys
sys.setrecursionlimit(3000)
seed = 0

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

def dtrunc (x: float) -> float:
    """ Truncar un numero float """

    k = int(x)
    x = float(k) # numero float sin parte decimal
    return x

def printSolToFile(outputFile: str, tour: list) -> None:
    """ Guardar la solucion para una instacia y ejecucion en un archivo recibido por parametro """
    if not outputFile or not tour:
        return
    try:
        print(f"{bcolors.OKGREEN}\nGuardando solucion en archivo... {bcolors.ENDC}{outputFile}")
        # Abrir archivo para escribir o reemplazar
        file = open(outputFile, 'w')
        # crear texto con la solucion separando cada elemento con espacios y luego guardarlo en el archivo
        sol = " ".join([str(elem) for elem in tour])
        file.write(sol)
        file.close()
    except IOError:
        print(f"{bcolors.FAIL}No se pudo guardar el archivo... {outputFile} Error: {IOError}{bcolors.ENDC}")

def printTraToFile(trajectoryFile: str, trajectory: list) -> None:
    """ Guardar la trayectoria de una solucion para una instacia y ejecucion en un archivo recibido por parametro """
    if not trajectoryFile or not trajectoryFile:
        return
    try:
        print(f"{bcolors.OKGREEN}\nGuardando trayectoria de la solucion en archivo... {bcolors.ENDC}{trajectoryFile}")
        # Abrir archivo para escribir o reemplazar
        file = open(trajectoryFile, 'w')
        # crear texto con la solucion separando cada elemento con espacios y luego guardarlo en el archivo
        for tour in trajectory:
            sol = " ".join([str(elem) for elem in tour])
            sol += '\n'
            file.write(sol)
        file.close()
    except IOError:
        print(f"{bcolors.FAIL}No se pudo guardar el archivo... {trajectoryFile} Error: {IOError}{bcolors.ENDC}")