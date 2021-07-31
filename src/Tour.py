from enum import Enum
from src.Utilities import bcolors

class InitialSolution(Enum):
    """ Metodos disponibles para crear una solucion inicial
    RANDOM: Solucion aleatoria
    NEAREST_N: Solucion creada con la heuristica del vecino mas cercano
    DETERMINISTIC: Solucion creada deterministicamente para testing, en este caso es secuencial
    """
    RANDOM = 'RANDOM'
    NEAREST_N = 'NEAREST_N'
    DETERMINISTIC = 'DETERMINISTIC'

class Tour():


    # Instancia del problema
    problema = None
    # Solucion actual
    actual = []
    costo = 0

    def __init__(self, **kwargs) -> None:

        if ('problema' in kwargs):
            self.problema = kwargs['problema']
        
        if ('sol_inicial' in kwargs):
            if (kwargs['sol_inicial'] == InitialSolution.RANDOM):
                self.actual = self.problema.random_tour()
            elif (kwargs['sol_inicial'] == InitialSolution.NEAREST_N):
                self.actual = self.problema.greedy_nearest_n(-1)
            elif (kwargs['sol_inicial'] == InitialSolution.DETERMINISTIC):
                self.actual = self.problema.deterministic_tour()
            else:
                self.actual = self.problema.random_tour()
        
        if (not self.problema.tsp_check_tour(self.actual)):
            print(f"{bcolors.FAIL}Error: Error al inicializar la solucion inicial {bcolors.ENDC}")
            exit()
        # Determinar costo de la solucion inicial
        self.costo = self.problema.compute_tour_length(self.actual)

        # si viene otra instancia de la clase como parametro definido
        if ('tour' in kwargs):
            # actualizar problema
            self.problema = kwargs['tour'].problema
            # copiar solucion actual
            self.actual = kwargs['tour'].actual.copy()
            # actualizar costo
            self.costo = kwargs['tour'].costo

    def Copy(self, tour) -> None:
        """ Copia una solicion recibida por parametro """
        self.actual = tour.copy()
        self.costo = tour.costo

