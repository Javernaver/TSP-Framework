from src.Utilities import bcolors, random
from src.AlgorithmsOptions import AlgorithmsOptions, TSPMove, CoolingType
from src.TSP import TSP
from src.Tour import Tour
from math import e, log
from timeit import default_timer as timer
import csv
from datetime import datetime
from pathlib import Path

class SimulatedAnnealing():
    
    # Problema 
    problem :TSP
    # Esquema de enfriamiento
    cooling :CoolingType
    # Tipo de movimiento
    move_type :TSPMove
    # Parametro alfa para el esquema de enfriamiento geometrico
    alpha = 0.0
    # Mejor tour 
    best_tour :Tour

    # numero de evaluacion
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
            self.problem = TSP(options.instance)
        else:
            self.problem = problem

        self.cooling = options.cooling
        self.move_type = options.move
        self.alpha = options.alpha
        
        self.best_tour = Tour(problem=self.problem, type_initial_sol=self.options.initial_solution)

        print(f"{bcolors.HEADER}\nIniciando Simulated Annealing...{bcolors.ENDC}")

    def print_best_solution(self) -> None:
        """ Escribir la mejor solucion """
        print()
        print(f"\t\t{bcolors.UNDERLINE}Mejor Solucion Encontrada{bcolors.ENDC}\n")
        self.best_tour.printSol()
        print(f"{bcolors.BOLD}Total de evaluaciones:{bcolors.ENDC} {bcolors.OKBLUE}{self.evaluations-1}{bcolors.ENDC}")
        self.updateTrajectory()

    def search(self, first_solution :Tour = None) -> None:
        """ Esta funcion ejecuta la busqueda de simulated annealing desde la solucion inicial
        (initial_solution, el resultadofinal puede ser encontrado en best_tour) """

        # Si el atributo opcional de la solucion inicial no esta incluido
        if not first_solution:
            first_solution = Tour(type_initial_sol=self.options.initial_solution, problem=self.problem)

        # variable de temperatura
        temperature = self.options.t0
        
        # variable para calculos de probabilidad 
        prob = 0.0        

        # variable del tour actual 
        current_tour = Tour(tour=first_solution);
        # variable del tour vecino generado 
        neighbor_tour = Tour(tour=first_solution);
        # solucion inicial se guarda como la mejor hasta el momento 
        self.best_tour.duplicate(first_solution);

        print(f"{bcolors.UNDERLINE}\nComenzando busqueda, solucion inicial: {bcolors.ENDC}")
        self.best_tour.printSol()

        # tiempo inicial de iteraciones
        start = timer()
        if not self.options.silent:
            print(f"{bcolors.BOLD}\nEvaluacion | Temperatura | Tiempo | Detalle{bcolors.ENDC}", end='')
        else: print(f"{bcolors.BOLD}\nEjecutando Simulated Annealing...{bcolors.ENDC}")
        # Bucle principal del algoritmo
        while (self.terminationCondition(temperature, self.evaluations)):
            # Generar un vecino aleatoriamente
            neighbor_tour.randomNeighbor(self.move_type)

            # tiempo actual de iteracion
            end = timer()
            if not self.options.silent:
                print(f"{bcolors.BOLD}\n{self.evaluations}; {temperature:.2f}; {end-start:.4f}{bcolors.ENDC};", end='')

            # Revisar funcion objetivo de la nueva solucion
            if (neighbor_tour.cost < current_tour.cost):
                # Mejor solucion encontrada
                current_tour.duplicate(neighbor_tour)
                if not self.options.silent:
                    print(f"{bcolors.OKGREEN} Solucion actual con mejor costo encontrada: {current_tour.cost}{bcolors.ENDC}", end='')
            else:
                # Calcular criterio de aceptacion
                prob = self.getAcceptanceProbability(neighbor_tour.cost, current_tour.cost, temperature)

                if (random.random() <= prob):
                    # Se acepta la solucion peor
                    current_tour.duplicate(neighbor_tour)
                    if not self.options.silent:
                        print(f"{bcolors.FAIL} Se acepta peor costo por criterio de metropolis: {neighbor_tour.cost}{bcolors.ENDC}", end='')
                else:
                    # No se acepta la solucion
                    if not self.options.silent:
                        print(f"{bcolors.WARNING} No se acepta peor costo por criterio de metropolis: {neighbor_tour.cost}{bcolors.ENDC}{bcolors.OKGREEN} --> Costo solucion actual: {current_tour.cost}{bcolors.ENDC}", end='')
                    neighbor_tour.duplicate(current_tour)

			
			# Revisar si la nueva solucion es la mejor hasta el momento
            if (current_tour.cost < self.best_tour.cost):
                if not self.options.silent:
                    print(f"{bcolors.OKGREEN} --> ¡Mejor solucion global encontrada! {bcolors.ENDC}", end='')
                self.best_tour.duplicate(current_tour)
                    
            # reducir la temperatura y aumentar las evaluaciones
            temperature = self.reduceTemperature(temperature, self.evaluations)
            self.evaluations += 1
        print()   
		

    def terminationCondition(self, termperature :float, evaluations :int) -> bool:
        """ Funcion que contiene la condicion de termino para el ciclo principal de Simulated Annealing """
        # Criterio de termino de la temperatura
        if (self.options.tmin > 0):
            if (termperature <= self.options.tmin):
                return False
		
        # Criterio de termino de las evaluciones
        if (self.options.max_evaluations > 0):
            if (evaluations > self.options.max_evaluations):
                return False
        
        return True
		

    def getAcceptanceProbability (self, neighbor_cost :int, current_cost :int, temperature :float) -> float:
        """ Funcion para obtener una probabilidad aplicando el criterio de metropolis e^-(delta/temp)"""
        # determinar delta
        delta = neighbor_cost - current_cost
        # Aplicar y retornar la formula para el criterio de metropolis
        return e**-(delta / temperature) 


    def reduceTemperature(self, temperature :float, evaluation :int) -> float:
        """ Funcion que reduce la temperatura de Simulated Annealing"""
        t_new = temperature
        if (self.cooling == CoolingType.GEOMETRIC):
            t_new *= self.options.alpha
        elif (self.cooling == CoolingType.LINEAR):
            t_new = self.options.t0 * (1 - (evaluation / self.options.max_evaluations))
        elif (self.cooling == CoolingType.LOG):
            t_new = (self.options.t0 * self.options.alpha) * (1 / log(evaluation+1))

        return t_new

    def printSolFile(self, filename :str) -> None:
        """ Guarda la solucion en archivo de texto"""
        self.best_tour.printToFile(filename)

    def updateTrajectory(self) -> None:
        """ Actualiza el registro de mejores soluciones con todas las caracteristicas de su ejecución """
        # crea la carpeta en caso de que no exista (python 3.5+)
        Path("trajectory/").mkdir(exist_ok=True)
        # usar el archivo en modo append
        with open("trajectory/SATrajectory.csv", "a", newline="\n") as csvfile:
            
            fields = ["solution","cost","instance","date","alpha","t0","tmin","cooling","seed","move","max_evaluations","initial_solution"]
            writer = csv.DictWriter(csvfile, fieldnames=fields)
            # Si la posicion de el archivo es cero se escriben los headers
            if not csvfile.tell():
                writer.writeheader()

            # crear texto con la solucion separando cada elemento con espacios y luego guardarlo en el archivo
            sol = " ".join([str(elem) for elem in self.best_tour.current])

            # escribir la mejor solucion y todas las caracteristicas de su ejecucion
            writer.writerow({"solution": sol, "cost": self.best_tour.cost, "instance": self.options.instance, "date": datetime.today(), "alpha": self.options.alpha, "t0": self.options.t0, "tmin": self.options.tmin, "cooling": self.options.cooling.value, "seed": self.options.seed, "move": self.options.move.value, "max_evaluations": self.options.max_evaluations, "initial_solution": self.options.initial_solution.value})