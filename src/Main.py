from src.Utilities import bcolors
from src.Tour import Tour
from src.AlgorithmsOptions import AlgorithmsOptions, MHType, TSPMove
from src.TSP import TSP
from src.SimulatedAnnealing.SimulatedAnnealing import SimulatedAnnealing
import sys
from timeit import default_timer as timer

class Main():
    """
    Clase principal que implementa algoritmos metaheristicos para resolver el problema del vendedor viajero (TSP)

    Methods
    -------
    __init__(argv=sys.argv)
        Clase principal que recibe los argumentos que puedan haber sido incluidos al ejecutar el script en la consola
    """
    def __init__(self, argv=sys.argv) -> None:
        """
        Clase principal que recibe los argumentos que puedan haber sido incluidos al ejecutar el script en la consola

        Parameters
        ----------
        argv : list of str, optional
            Lista con los argumentos que pueda tener al inicializar la clase

        """
        # tiempo inicial de ejecucion
        start = timer()
        # leer e inicializar las opciones 
        options = AlgorithmsOptions(argv)

        # leer e interpretar el problema TSP leido desde la instancia definida
        problem = TSP(options.instance)
        #print(problema.random_tour())

        first_solution = Tour(type_initial_sol=options.initial_solution, problem=problem)
        #print(solucion_inicial.actual, solucion_inicial.costo)
        #solucion_inicial.randomNeighbor(TSPMove.TWO_OPT)
        #print(solucion_inicial.actual, solucion_inicial.costo)

        # Ejecutar Metaheuristica
        if (options.metaheuristic == MHType.SA):
            # Crear solver
            solver = SimulatedAnnealing(options, problem)
            # Ejecutar la busqueda
            solver.search(first_solution)
            solver.print_best_solution()

        # tiempo final de ejecucion
        end = timer()
        print(f"{bcolors.BOLD}Tiempo total de ejecución: {bcolors.ENDC}{bcolors.OKBLUE} {end-start:.2f} segundos{bcolors.ENDC}")