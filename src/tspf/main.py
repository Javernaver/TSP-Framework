"""
Modulo principal que utiliza todas las demas clases para ejecutar el framework

"""

from .Algorithms import GeneticAlgorithm, SimulatedAnnealing, LocalSearch, IteratedLocalSearch, timer
from .Tools import bcolors, gui
from . import sys, os, AlgorithmsOptions, MHType, Tsp, Tour

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
    
    # Si se esta en modo GUI
    if options.gui:
        gui.main(options)
        return
        
    # Mostrar Opciones 
    options.printOptions()

    # leer e interpretar el problema TSP leido desde la instancia definida
    problem = Tsp(filename=options.instance)

    # Ejecutar Simulated Annealing
    if (options.metaheuristic == MHType.SA):

        # Solucion inicial
        first_solution = Tour(type_initial_sol=options.initial_solution, problem=problem)
        # Crear solver
        solver = SimulatedAnnealing(options=options, problem=problem)
        # Ejecutar la busqueda
        solver.search(first_solution)

    # Ejecutar Algoritmo Genetico
    elif (options.metaheuristic == MHType.GA):
        # Crear solver
        solver = GeneticAlgorithm(options=options, problem=problem)
        # Ejecutar la busqueda
        solver.search()
    
    # Ejecutar Local Search    
    elif (options.metaheuristic == MHType.LS):
        # Solucion inicial
        first_solution = Tour(type_initial_sol=options.initial_solution, problem=problem)
        # Crear solver
        solver = LocalSearch(options=options, problem=problem)
        # Ejecutar la busqueda
        solver.search(first_solution)
    
    # Ejecutar Iterated Local Search    
    elif (options.metaheuristic == MHType.ILS):
        # Solucion inicial
        first_solution = Tour(type_initial_sol=options.initial_solution, problem=problem)
        # Crear solver
        solver = IteratedLocalSearch(options=options, problem=problem)
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
    print(f"{bcolors.BOLD}Tiempo total de ejecución: {bcolors.ENDC}{bcolors.OKBLUE} {end-start:.3f} segundos{bcolors.ENDC}")
    
    if options.visualize:
        solver.visualize()
 