import csv
from datetime import datetime
from pathlib import Path
from timeit import default_timer as timer

from src.Algorithms.Population import Population
from src.Utilities import bcolors
from src.Tour import Tour
from src.TSP import TSP
from src.AlgorithmsOptions import AlgorithmsOptions, SelectionStrategy, SelectionType, CrossoverType, MutationType


class GeneticAlgorithm():

    def __init__(self, options: AlgorithmsOptions = None, problem: TSP = None) -> None:

        # Atributos de instancia
        self.problem: TSP # Problema 	
    
        self.pop_size = 10 # Parametro tamaño de la poblacion 	
        
        self.offspring_size = 20	# Cantidad de hijos
        
        self.pselection_type = SelectionType.RANDOM # Seleccion de padres
        
        self.crossover_type = CrossoverType.OX # Cruzamiento 	
        
        self.mutation_type = MutationType.SWAP # Mutacion	
        
        self.mutation_prob = 0.2 # Probabilidad de mutacion
        
        self.selection_strategy = SelectionStrategy.MULAMBDA # Estrategia de seleccion de la nueva poblacion
        
        self.gselection_type = SelectionType.RANDOM # Tipo de seleccion de la poblacion
        
        self.elitism = 0 # Soluciones seleccionadas por elitismo 

        self.best_tour: Tour = None # Mejor tour 
        
        self.total_time = 0.0 # tiempo de ejecucion de Algoritmo Genetico
        
        self.iterations = 1 # numero de iteraciones
        
        self.evaluations = 1 # numero de evaluaciones

        self.options: AlgorithmsOptions # Opciones

        self.total_time = 0.0 # tiempo de ejecucion de Algoritmo Genetico

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

        self.pop_size = self.options.pop_size # Parametro tamaño de la poblacion 

        self.offspring_size = self.options.offspring_size # Cantidad de hijos

        self.pselection_type = self.options.pselection_type # Seleccion de padres

        self.crossover_type = self.options.crossover_type # Cruzamiento

        self.mutation_type = self.options.mutation_type # Mutacion

        self.mutation_prob = self.options.mutation_prob # Probabilidad de mutacion

        self.selection_strategy = self.options.selection_strategy # Estrategia de seleccion de la nueva poblacion

        self.gselection_type = self.options.gselection_type # Tipo de seleccion de la poblacion

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
        print(f"{bcolors.BOLD}Generando poblacion inicial...{bcolors.ENDC}")
        population = Population(pop_size=self.pop_size, problem=self.problem)
        # Iniciar poblacion de hijos
        offspring = Population(problem=self.problem)
        #population.printPop()
        
        i =0 
        for tour in population.pop:
            print(tour.cost, i)
            i+=1

        # Imprimir mejor solución encontrada 
        print(f"{bcolors.UNDERLINE}Mejor individuo de la poblacion{bcolors.ENDC}")
        population.getBestTour().printSol()
        
        # Guardar la mejor solución en best_tour
        if not self.best_tour:
            self.best_tour = Tour(tour=population.getBestTour())
        else:
            self.best_tour.copy(population.getBestTour())
  
        # tiempo para iteraciones y condicion de termino por tiempo
        start = end = timer()

        # bucle principal de Algoritmo Genetico
        print(f"{bcolors.HEADER}\nComenzando Busqueda con Algoritmo Generico...\n{bcolors.ENDC}")

        # Bucle principal del algoritmo
        while (self.terminationCondition(self.iterations, self.evaluations, end-start)):
            
            end = timer() # tiempo actual de iteracion
            i = 0
            # Aplicar cruzamiento para generar poblacion de hijos
            while (offspring.pop_size < self.offspring_size):
                parents = population.selectParents(self.pselection_type)
                
                print(parents, i)
                i+=1
                offspring.pop_size += 1
                

          
            # Actualizar contadores de iteraciones y evaluaciones, luego limpiar la poblacion de hijos
            self.evaluations += self.offspring_size
            self.iterations += 1
            offspring.clear()


    def terminationCondition(self, iterations: int, evaluations: int, time: float) -> bool:
        """ Condicion de termino para el ciclo principal de Algoritmo Genetico, 
        basado en los criterios de iteraciones, evaluaciones y tiempo, devuelve verdadero o falso si se debe continuar o no"""
        # Criterio de termino de las iteraciones
        if (self.options.max_iterations > 0):
            if (iterations > self.options.max_iterations):
                return False
        # Criterio de termino de las evaluciones
        if (self.options.max_evaluations > 0):
            if (evaluations > self.options.max_evaluations):
                return False

        # Criterio de termino por tiempo
        if (self.options.max_time > 0):
            if (time > self.options.max_time):
                return False
        
        return True

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