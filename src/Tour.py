from src.TSP import TSP
from src.AlgorithmsOptions import InitialSolution, TSPMove
from src.Utilities import bcolors
import src.Utilities as util

class Tour():

    # Instancia del problema
    problema = TSP
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

        # Si viene otra instancia de la clase como parametro definido
        if ('tour' in kwargs):
            # actualizar problema
            self.problema = kwargs['tour'].problema
            # copiar solucion actual
            self.actual = kwargs['tour'].actual.copy()
            # actualizar costo
            self.costo = kwargs['tour'].costo

    def copiar(self, tour: list) -> None:
        """ Copia una solicion recibida por parametro actualizando la solucion actual """
        self.actual = tour.copy()
        self.costo = tour.costo

    def escribir(self) -> None:
        """ Escribir solucion y costo """
        self.problema.print_solution_and_cost(self.actual)

    def escribirCosto(self) -> None:
        """ Escribe el costo de un tour """
        print(f"Costo: {self.costo}", end='')

    def delta_cost_swap(self, tour: list, cost: int, n1: int, n2: int) -> int:
        """ Recalcula el costo de un tour al aplicar el movimiento swap  

        Input
        -----
        tour: list
            Lista del tour a modificar (sin haber sido modificado aun),
        cost: int
            El costo actual del tour
        n1, n2: int
            Indices de los nodos para hacer swap

        Output
        ------
            El nuevo costo luego de aplicar swap
        """
     
        # Si es el mismo nodo, no hay swap
        if (n1 == n2): return cost
        # Indice fuera de los limites
        if (n1 >= self.problema.getSize() or n2 >= self.problema.getSize()): return cost
        if (n1 < 0 or n2 < 0): return cost
        
        # Identificar el indice menor y el mayor
        s = min(n1, n2)
        e = max(n1, n2)

        # Identificar nodos anteriores y posteriores para formar los bordes 
        s_prev = s - 1
        s_next = s + 1
        e_prev = e - 1
        e_next = e + 1

        if (s == 0):
            s_prev = self.problema.getSize() - 1
        if (e == self.problema.getSize() - 1):
            e_next = 0

        # Calcular nuevo costo
        if (s_prev != e):
            cost = cost - self.problema.get_distance(tour[s_prev], tour[s]) - self.problema.get_distance(tour[e], tour[e_next]) + self.problema.get_distance(tour[s_prev], tour[e]) + self.problema.get_distance(tour[s], tour[e_next])
        else:
            cost = cost - self.problema.get_distance(tour[s], tour[s_next]) - self.problema.get_distance(tour[e_prev], tour[e]) + self.problema.get_distance(tour[e], tour[s_next]) + self.problema.get_distance(tour[e_prev], tour[s])
        
        if (s_next != e_next and s_next != e and s_prev != e):
            cost = cost - self.problema.get_distance(tour[s], tour[s_next]) - self.problema.get_distance(tour[e_prev], tour[e]) + self.problema.get_distance(tour[e], tour[s_next]) + self.problema.get_distance(tour[e_prev], tour[s])
        
        return cost

    def swap(self, n1: int, n2: int) -> None:
        """ Aplica el movimiento swap entre dos nodos modificando la solucion actual y su costo """
        # Si es el mismo nodo, no hay swap
        if (n1 == n2): return
        # Indice fuera de los limites
        if (n1 >= self.problema.getSize() or n2 >= self.problema.getSize()): return
        if (n1 < 0 or n2 < 0): return

        tour = self.actual.copy()

        # Aplicar SWAP
        tour[n1], tour[n2] = tour[n2], tour[n1]
        # Igualar inicio y final
        tour[len(tour)-1] = tour[0]
        # Actualizar costo y tour
        self.costo = self.delta_cost_swap(self.actual, self.costo, n1, n2)
        self.actual = tour.copy()

    def delta_cost_two_opt(self, tour: list, cost: int, s: int, e: int) -> int:
        """ Recalcula el costo de un tour al alplicar el movimiento 2-opt    

        Input
        -----
        tour: list
            Lista del tour a modificar (sin haber sido modificado aun),
        cost: int
            El costo actual del tour
        s, e: int
            Indices de los nodos para ser intercambiardos con 2-opt

        Output
        ------
            El nuevo costo luego de aplicar 2-opt
        """

        # Si es el mismo nodo, no hay swap
        if (e == s): return cost
        # Indice fuera de los limites
        if (s >= self.problema.getSize() or e >= self.problema.getSize()): return cost
        if (s < 0 or e < 0): return cost

        # Identificar el nodo anterior y posterior para formar los caminos
        s_prev = s - 1
        e_next = e + 1
        
        if (s == 0):
            if (e == self.problema.getSize()-1): return cost
            s_prev = self.problema.getSize()-1

        # Calcular nuevo costo
        cost = cost - self.problema.get_distance(tour[s_prev], tour[s]) - self.problema.get_distance(tour[e], tour[e_next]) + self.problema.get_distance(tour[s_prev], tour[e]) + self.problema.get_distance(tour[s], tour[e_next])

        return cost
    
    def twoOptSwap(self, n1: int, n2: int) -> None:
        """ Aplica el movimiento 2-opt entre dos nodos modificando la solucion actual y su costo"""
        # Si es el mismo nodo, no hay swap
        if (n1 == n2): return
        # Indice fuera de los limites
        if (n1 >= self.problema.getSize() or n2 >= self.problema.getSize()): return
        if (n1 < 0 or n2 < 0): return

        # Identificar el indice menor y el mayor
        s = min(n1, n2)
        e = max(n1, n2)
        new_tour = [0] * len(self.actual)

        # Copiar la primera parte del tour no modificado por 2-opt
        for i in range(s):
            new_tour[i] = self.actual[i]
        
        # invertir el orden del tour entre [s,e] 
        aux = 0;
        for i in range(s,e+1):
            new_tour[i] = self.actual[e-aux] # intercambiar nodos
            aux += 1

        # Copiar la parte final del tour no modificado por 2-opt 
        for i in range(e+1, len(self.actual)):
            new_tour[i] = self.actual[i]

        # Igualar inicio y final
        new_tour[len(self.actual)-1] = new_tour[0]
        
        # Actualizar costo y tour
        self.costo = self.delta_cost_two_opt(self.actual, self.costo, s, e)
        self.actual = new_tour.copy()
        
    def randomNeighbor(self, move_type: TSPMove):
        """ Aplica un movimiento aleatorio recibido por parametro del tipo TSPMove"""
        
        n1 = n2 = util.random.randint(0, self.problema.getSize())
        # Determinar que sean numeros diferentes
        while (n1 == n2):
            n2 = util.random.randint(0, self.problema.getSize())

        # Seleccionar el tipo de movimiento
        if (move_type == TSPMove.TWO_OPT):
            self.twoOptSwap(n1, n2)
        elif (move_type == TSPMove.SWAP):
            self.swap(n1, n2)
        else:
            self.swap(n1, n2)
