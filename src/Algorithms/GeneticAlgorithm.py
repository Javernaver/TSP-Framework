import csv
from datetime import datetime
from pathlib import Path
from src.Algorithms.Population import Population

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


    def search(self) -> None:
        """ Ejecuta la busqueda del Algoritmo Genetico desde una poblacion generada aleatoriamente """
        
        parents = []
        # Inicializar poblacion
        print(f"{bcolors.BOLD}Generando poblacion inicial ...{bcolors.ENDC}{bcolors.ENDC}")
        
        population = Population(pop_size=self.pop_size, problem=self.problem)
        #for i in population.pop:
         #   print(i.cost)

    def updateTrajectory(self) -> None:
        """ Actualiza el registro de mejores soluciones con todas las caracteristicas de su ejecución """
        # crea la carpeta en caso de que no exista (python 3.5+)
        Path("trajectory/").mkdir(exist_ok=True)
        # usar el archivo en modo append
        with open("trajectory/GATrajectory.csv", "a", newline="\n") as csvfile:
            
            fields = ["solution","cost","instance","date","pop_size","offspring_size","pselection_type","crossover_type","mutation_type","mutation_prob","selection_strategy","gselection_type","seed","move","max_evaluations","initial_solution"]
            writer = csv.DictWriter(csvfile, delimiter=';', fieldnames=fields)
            # Si la posicion de el archivo es cero se escriben los headers
            if not csvfile.tell():
                writer.writeheader()

            # crear texto con la solucion separando cada elemento con espacios y luego guardarlo en el archivo
            sol = " ".join([str(elem) for elem in self.best_tour.current])

            # escribir la mejor solucion y todas las caracteristicas de su ejecucion
            writer.writerow({"solution": sol, "cost": self.best_tour.cost, "instance": self.options.instance, "date": datetime.today(), "pop_size": self.options.pop_size, "offspring_size": self.options.offspring_size, "pselection_type": self.options.pselection_type.value, "crossover_type": self.options.crossover_type.value, "mutation_type": self.options.mutation_type.value, "mutation_prob": self.options.mutation_prob, "selection_strategy": self.options.selection_strategy.value, "gselection_type": self.options.gselection_type.value, "seed": self.options.seed, "move": self.options.move.value, "max_evaluations": self.options.max_evaluations,"max_iterations": self.options.max_iterations,"max_time": self.options.max_time, "initial_solution": self.options.initial_solution.value})