from src.Utilities import bcolors
from src.Tour import Tour
from src.TSP import TSP
from src.AlgorithmsOptions import AlgorithmsOptions, SelectionStrategy, SelectionType, CrossoverType, MutationType


class GeneticAlgorithm():

    # Problema 
    problem: TSP	
    # Parametro tamaño de la poblacion 
    pop_size = 10	
    # Cantidad de hijos
    offspring_size = 20	
    # Seleccion de padres 
    pselection_type = SelectionType.RANDOM	
    # Cruzamiento 
    crossover_type = CrossoverType.OX	
    # Mutacion 
    mutation_type = MutationType.SWAP	
    # Probabilidad de mutacion 
    mutation_prob = 0.2
    # Estrategia de seleccion de la nueva poblacion 
    selection_strategy = SelectionStrategy.MULAMBDA
    # Tipo de seleccion de la poblacion
    gselection_type = SelectionType.RANDOM

    # Soluciones seleccionadas por elitismo 
    elitism = 0

    # Mejor tour 
    best_tour :Tour
    # tiempo de ejecucion de Algoritmo Genetico
    total_time = 0.0
    # numero de iteraciones
    iterations = 1
    # numero de evaluaciones
    evaluations = 1

    # Opciones
    options :AlgorithmsOptions

    def __init__(self, options: AlgorithmsOptions = None, problem: TSP = None) -> None:
        # Si por el objeto con las opciones no es enviado al iniciar la clase
        if not options:
            self.options = AlgorithmsOptions()
        else:
            self.options = options
        # Si el objeto con el problema tsp no esta incluido
        if not problem:
            self.problem = TSP(self.options.instance)
        else:
            self.problem = problem

        self.pop_size = self.options.pop_size
        self.offspring_size = self.options.offspring_size
        self.pselection_type = self.options.pselection_type
        self.crossover_type = self.options.crossover_type
        self.mutation_type = self.options.mutation_type
        self.mutation_prob = self.options.mutation_prob
        self.selection_strategy = self.options.selection_strategy
        self.gselection_type = self.options.gselection_type

        print(f"{bcolors.HEADER}\nIniciando Algortimo Genetico...{bcolors.ENDC}")


    def print_best_solution(self) -> None:
        """ Escribir la mejor solucion """
        print()
        print(f"\t\t{bcolors.UNDERLINE}Mejor Solucion Encontrada{bcolors.ENDC}\n")
        self.best_tour.printSol()
        print(f"{bcolors.BOLD}Total de iteraciones:{bcolors.ENDC} {bcolors.OKBLUE}{self.iterations-1}{bcolors.ENDC}")
        print(f"{bcolors.BOLD}Total de evaluaciones:{bcolors.ENDC} {bcolors.OKBLUE}{self.evaluations-1}{bcolors.ENDC}")
        print(f"{bcolors.BOLD}Tiempo total de ejecucion de Algoritmo Genetico:{bcolors.ENDC} {bcolors.OKBLUE}{self.total_time:.2f} segundos{bcolors.ENDC}")
        self.updateTrajectory()