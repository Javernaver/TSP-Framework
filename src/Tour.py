from src.TSP import TSP
from src.AlgorithmsOptions import InitialSolution, TSPMove
from src.Utilities import bcolors
import src.Utilities as util

class Tour():
 
    def __init__(self, **kwargs) -> None:

        # Atributos de instancia
        self.problem: TSP # Instancia del problema
    
        self.current = [] # Solucion actual

        self.cost = 0 # costo solucion actual

        # Ssi trae el problema TSP
        if ('problem' in kwargs):
            self.problem = kwargs['problem']
        
        if ('type_initial_sol' in kwargs):
            if (kwargs['type_initial_sol'] == InitialSolution.RANDOM):
                self.current = self.problem.random_tour()
            elif (kwargs['type_initial_sol'] == InitialSolution.NEAREST_N):
                self.current = self.problem.greedy_nearest_n(0)
            elif (kwargs['type_initial_sol'] == InitialSolution.DETERMINISTIC):
                self.current = self.problem.deterministic_tour()
            else:
                self.current = self.problem.random_tour()
        
        # Si viene otra instancia de la clase como parametro definido
        if ('tour' in kwargs):
            # actualizar problema
            self.problem = kwargs['tour'].problem
            # copiar solucion actual
            self.current = kwargs['tour'].current.copy()
            # actualizar costo
            self.cost = kwargs['tour'].cost

        if (not self.problem.tsp_check_tour(self.current)):
            print(f"{bcolors.FAIL}Error: Error al inicializar la solucion inicial {bcolors.ENDC}")
            exit()

        # Determinar costo de la solucion inicial
        self.cost = self.problem.compute_tour_length(self.current)

    def copy(self, tour: 'Tour') -> None:
        """ Copia una solucion de otra instancia del objeto recibida por parametro actualizando la solucion actual """
        self.current = tour.current.copy()
        self.cost = tour.cost

    def printSol(self) -> None:
        """ Escribir solucion y costo """
        self.problem.print_solution_and_cost(self.current)

    def printCost(self) -> None:
        """ Escribe el costo de un tour """
        print(f"Costo: {self.cost}", end='')

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
        if (n1 >= self.problem.getSize() or n2 >= self.problem.getSize()): return cost
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
            s_prev = self.problem.getSize() - 1
        if (e == self.problem.getSize() - 1):
            e_next = 0

        # Calcular nuevo costo
        if (s_prev != e):
            cost = cost - self.problem.get_distance(tour[s_prev], tour[s]) - self.problem.get_distance(tour[e], tour[e_next]) + self.problem.get_distance(tour[s_prev], tour[e]) + self.problem.get_distance(tour[s], tour[e_next])
        else:
            cost = cost - self.problem.get_distance(tour[s], tour[s_next]) - self.problem.get_distance(tour[e_prev], tour[e]) + self.problem.get_distance(tour[e], tour[s_next]) + self.problem.get_distance(tour[e_prev], tour[s])
        
        if (s_next != e_next and s_next != e and s_prev != e):
            cost = cost - self.problem.get_distance(tour[s], tour[s_next]) - self.problem.get_distance(tour[e_prev], tour[e]) + self.problem.get_distance(tour[e], tour[s_next]) + self.problem.get_distance(tour[e_prev], tour[s])
        
        return cost

    def swap(self, n1: int, n2: int) -> None:
        """ Aplica el movimiento swap entre dos nodos modificando la solucion actual y su costo """
        # Si es el mismo nodo, no hay swap
        if (n1 == n2): return
        # Indice fuera de los limites
        if (n1 >= self.problem.getSize() or n2 >= self.problem.getSize()): return
        if (n1 < 0 or n2 < 0): return

        tour = self.current.copy()

        # Aplicar SWAP
        tour[n1], tour[n2] = tour[n2], tour[n1]
        # Igualar inicio y final
        tour[len(tour)-1] = tour[0]
        # Actualizar costo y tour
        self.cost = self.delta_cost_swap(self.current, self.cost, n1, n2)
        self.current = tour.copy()

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
        if (s >= self.problem.getSize() or e >= self.problem.getSize()): return cost
        if (s < 0 or e < 0): return cost

        # Identificar el nodo anterior y posterior para formar los caminos
        s_prev = s - 1
        e_next = e + 1
        
        if (s == 0):
            if (e == self.problem.getSize()-1): return cost
            s_prev = self.problem.getSize()-1

        # Calcular nuevo costo
        cost = cost - self.problem.get_distance(tour[s_prev], tour[s]) - self.problem.get_distance(tour[e], tour[e_next]) + self.problem.get_distance(tour[s_prev], tour[e]) + self.problem.get_distance(tour[s], tour[e_next])

        return cost
    
    def twoOptSwap(self, n1: int, n2: int) -> None:
        """ Aplica el movimiento 2-opt entre dos nodos modificando la solucion actual y su costo"""
        # Si es el mismo nodo, no hay swap
        if (n1 == n2): return
        # Indice fuera de los limites
        if (n1 >= self.problem.getSize() or n2 >= self.problem.getSize()): return
        if (n1 < 0 or n2 < 0): return

        # Identificar el indice menor y el mayor
        s = min(n1, n2)
        e = max(n1, n2)
        new_tour = [0] * len(self.current)

        # Copiar la primera parte del tour no modificado por 2-opt
        for i in range(s):
            new_tour[i] = self.current[i]
        
        # invertir el orden del tour entre [s,e] 
        aux = 0
        for i in range(s,e+1):
            new_tour[i] = self.current[e-aux] # intercambiar nodos
            aux += 1

        # Copiar la parte final del tour no modificado por 2-opt 
        for i in range(e+1, len(self.current)):
            new_tour[i] = self.current[i]

        # Igualar inicio y final
        new_tour[len(self.current)-1] = new_tour[0]
        
        # Actualizar costo y tour
        self.cost = self.delta_cost_two_opt(self.current, self.cost, s, e)
        self.current = new_tour.copy()
        
    def randomNeighbor(self, move_type: TSPMove) -> None:
        """ Aplica un movimiento aleatorio recibido por parametro del tipo TSPMove"""
        
        n1 = n2 = util.random.randint(0, self.problem.getSize())
        # Determinar que sean numeros diferentes
        while (n1 == n2):
            n2 = util.random.randint(0, self.problem.getSize())

        # Seleccionar el tipo de movimiento
        if (move_type == TSPMove.TWO_OPT):
            self.twoOptSwap(n1, n2)
        elif (move_type == TSPMove.SWAP):
            self.swap(n1, n2)
        else:
            self.swap(n1, n2)

    def printToFile(self, filename: str) -> None:
        """ Guardar la solucion para una instacia y ejecucion en un archivo recibido por parametro """
        if not filename:
            return
        try:
            print(f"{bcolors.OKGREEN}\nGuardando solucion en archivo... {bcolors.ENDC}{filename}")
            # Abrir archivo para escribir o reemplazar
            file = open(filename, 'w')
            # crear texto con la solucion separando cada elemento con espacios y luego guardarlo en el archivo
            sol = " ".join([str(elem) for elem in self.current])
            file.write(sol)
            file.close()
        except IOError:
            print(f"{bcolors.FAIL}No se pudo guardar el archivo... {filename} Error: {IOError}{bcolors.ENDC}")