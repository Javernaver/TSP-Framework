"""Modulo principal que utiliza todas las demas clases para ejecutar el framework"""

from .Algorithms import GeneticAlgorithm, SimulatedAnnealing, LocalSearch, timer
from . import sys, os, AlgorithmsOptions, MHType, Tsp, Tour, bcolors

def main(argv=sys.argv) -> None:
    """
    Funcion principal que ejecuta el framework algoritmos metaheristicos para resolver el problema del vendedor viajero (TSP)

    """

    # Activa la secuencia VT100 en Windows 10 para que funcione ANSI y se puedan cambiar se color los textos en cmd y powershell
    os.system('')  
    #bcolors.disable(bcolors)
    start = timer() # tiempo inicial de ejecucion
    # leer e inicializar las opciones 
    options = AlgorithmsOptions(argv=argv)

    # leer e interpretar el problema TSP leido desde la instancia definida
    problem = Tsp(filename=options.instance)

    # Ejecutar Metaheuristica Simulated Annealing
    if (options.metaheuristic == MHType.SA):

        # Solucion inicial
        first_solution = Tour(type_initial_sol=options.initial_solution, problem=problem)
        # Crear solver
        solver = SimulatedAnnealing(options=options, problem=problem)
        # Ejecutar la busqueda
        solver.search(first_solution)

    # Ejecutar Metaheuristica Algoritmo Genetico
    elif (options.metaheuristic == MHType.GA):
        # Crear solver
        solver = GeneticAlgorithm(options=options, problem=problem)
        # Ejecutar la busqueda
        solver.search()
        
    elif (options.metaheuristic == MHType.LS):
        # Solucion inicial
        first_solution = Tour(type_initial_sol=options.initial_solution, problem=problem)
        # Crear solver
        solver = LocalSearch(options=options, problem=problem)
        # Ejecutar la busqueda
        solver.search(first_solution)

    else: 
        # Crear solver
        solver = GeneticAlgorithm(options=options, problem=problem)
        # Ejecutar la busqueda
        solver.search()

    # Guardar la solucion y trayectoria en archivo
    solver.printSolFile(options.solution)
    solver.printTraFile(options.trajectory)
    # Escribir la solucion por consola
    solver.print_best_solution()
    
    end = timer() # tiempo final de ejecucion
    print(f"{bcolors.BOLD}Tiempo total de ejecucion: {bcolors.ENDC}{bcolors.OKBLUE} {end-start:.3f} segundos{bcolors.ENDC}")
    
    if options.visualize:
        solver.visualize(options.replit)
 