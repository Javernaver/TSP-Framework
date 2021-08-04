from src.Utilities import bcolors
from src.AlgorithmsOptions import AlgorithmsOptions, TSPMove, CoolingType, InitialSolution
from src.TSP import TSP
from src.Tour import Tour

class SimulatedAnnealing():
    
    # Problema 
    problem = TSP
    # Esquema de enfriamiento
    cooling = CoolingType
    # Tipo de movimiento
    move_type = TSPMove
    # Parametro alfa para el esquema de enfriamiento geometrico
    alpha = 0.0
    # Mejor tour 
    best_tour = Tour

    def __init__(self, problem: TSP, options: AlgorithmsOptions) -> None:
        
        self.problem = problem
        self.cooling = options.cooling
        self.move_type = options.move
        self.alpha = options.alpha
        self.best_tour = Tour(problem=self.problem, initial_sol=InitialSolution.RANDOM)

        print(f"{bcolors.HEADER}\nIniciando Simulated Annealing...{bcolors.ENDC}")