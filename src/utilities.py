import random
import sys
import csv


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


class Trajectory():
    """ Clase cuyo fin es almacenar datos de la trayectoria recorrida por las soluciones de los algorimtos

        Parameters
        ----------
        tour : list
            lista con el recorrido
        cost : int
            calidad del recorrido
        iterations : int
            numero de iteraciones al llegar a la solucion
        evaluations : int
            numero de evaluaciones al llegar a la solucion
        average : float, optional
            promedio de las soluciones de la poblacion (Algoritmo Genetico)
        deviation : float, optional
            deviacion estandar de las soluciones de la poblacion (Algoritmo Genetico)
        temperature : float, optional
            temperatura al momemto de la solucion (simulated annealing)

        Examples
        --------
        >>> tra = Trajectory([0,1,2,3,4,5,6,7,8,9,0],
                            3542, 10, 15,
                            temperature=950.31)
    """
    def __init__(self, tour: list, cost: int, iterations: int,
                 evaluations: int, average: float = 0.0, deviation: float = 0.0,
                 temperature: float = 0.0) -> None:
        self.tour = tour
        self.cost = cost
        self.iterations = iterations
        self.evaluations = evaluations
        self.average = average # promedio
        self.deviation = deviation # desviacion estandar
        self.temperature = temperature

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
        csvfile = open(trajectoryFile, 'w', newline="\n")

        # Headers
        fields = ["Iterations","Evaluations","cost","solution"]
        writer = csv.DictWriter(csvfile, delimiter=';', fieldnames=fields)
        writer.writeheader()
        # crear texto con la solucion separando cada elemento con espacios y luego guardarlo en el archivo
        for tra in trajectory:
            sol = " ".join([str(elem) for elem in tra.tour])
            # escribir la mejor solucion y todas las caracteristicas de su ejecucion
            writer.writerow({
                "Iterations": tra.iterations, "Evaluations": tra.evaluations,
                "cost": tra.cost, 
                "solution": sol
            })

        csvfile.close()
    except IOError:
        print(f"{bcolors.FAIL}No se pudo guardar el archivo... {trajectoryFile} Error: {IOError}{bcolors.ENDC}")