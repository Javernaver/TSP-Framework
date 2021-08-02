from src.AlgorithmsOptions import AlgorithmsOptions
from src.Utilities import bcolors
from src.TSPlibReader import TSPlibReader
import src.Utilities as util

class TSP():
    """
    Clase que lee una instancia, evalua soluciones del TSP y provee metodos para crear soluciones

    Attributes
    ----------
    nodos : int
        Numero de Nodos
    distancia : list[list]
        Matriz con la distacia
    nn_list : int
        Matriz con vecinos mas cercanos
    tsplib_instance : TSPlibReader
        Instancia TSP
    opciones : AlgorithmsOptions
        Opciones
    

    Methods
    -------
    __init__(args, opciones)
        Clase constructora, lee todas las opciones que pueda tener el problema
   
    """

    # Numero de Nodos
    nodos = 0

    # Matriz con la distacia 
    distancia = [[]]

    # Matriz con vecinos mas cercanos 
    vecinos = [[]]

    # Instancia TSP
    instancia = None

    # Opciones
    opciones = None

    def __init__(self, opciones: AlgorithmsOptions) -> None:

        # leer opciones
        self.opciones = opciones

        # leer instancia desde un archivo TSPlib
        self.instancia = TSPlibReader(self.opciones.instance)

        # obtener matriz de distancia
        self.distancia = self.instancia.distance

        # obtener vecinos mas cercanos
        self.vecinos = self.instancia.nn_list
        
        # obtener tamano de la instancia 
        self.nodos = self.instancia.n
        #print(self.compute_tour_length([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 11, 13, 0]))
        #self.print_solution_and_cost([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 11, 13, 0])

        #self.print_distances()


    def getSize(self) -> int:
        """ Obtener numero de nodos"""
        return self.nodos

    def print_distances(self) -> None:
        """ Imprimir matriz de distancia entre nodos """
        print(f"{bcolors.BOLD}Distancia entre Nodos: {bcolors.ENDC}")
        for fila in self.distancia:
            for valor in fila:
                print(f"{bcolors.OKCYAN}{valor} {bcolors.ENDC}",end=" ")
            if fila: print()      

    def get_distance(self, i: int, j: int) -> list[list]:
        """ Obtener distancia entre los nodos por su indice i y j"""
        return self.distancia[i][j]

    def compute_tour_length(self, tour: list) -> int:
        """ Computar y retornar el costo de un tour """
        tour_length = 0
        for i in range(self.nodos):
            tour_length += self.distancia[tour[i]][tour[i + 1]]
        return tour_length

    def tsp_check_tour(self, tour: list) -> bool:
        """ Revisa la correctitud de una solucion del TSP """
        
        error = False
        used = [0] * self.nodos

        # Si no se recibio el tour 
        if (not tour):
            print(f"{bcolors.FAIL}Error: permutacion no esta inicializada! {bcolors.ENDC}")
            exit()

        for i in range(self.nodos):
            if used[tour[i]] != 0:
                print(f"{bcolors.FAIL}Error: la solucion tiene dos veces el valor {tour[i]} (ultima posicion: {i}) {bcolors.ENDC}")
                error = True
            else:
                used[tour[i]] = 1

        if (not error):
            for i in range(self.nodos):
                if (used[i] == 0):
                    print(f"{bcolors.FAIL}Error: posicion {i} en la solucion no esta ocupada{bcolors.ENDC}")
                    error = True
        if (not error):
            if (tour[0] != tour[self.nodos]):
                print(f"{bcolors.FAIL}Error: la permutacion no es un tour cerrado.{bcolors.ENDC}")
                error = True;
            
        if (not error):
            return True

        print(f"{bcolors.FAIL}Error: vector solucion:{bcolors.ENDC} ", end='')
        for i in range(self.nodos):
            print(f"{bcolors.FAIL}{tour[i]}{bcolors.ENDC}", end=" ")
        print()
        return False
        
    def print_solution_and_cost(self, tour: list) -> None:
        """ Muestra la solucion y costo """

        print(f"{bcolors.BOLD}Solucion: {bcolors.ENDC}", end='')
        for i in range(self.nodos+1):
            print(f"{bcolors.OKCYAN}{tour[i]}{bcolors.ENDC}", end=' ')
        print(f"{bcolors.BOLD}\nCosto: {bcolors.ENDC}{bcolors.OKCYAN}{self.compute_tour_length(tour)}{bcolors.ENDC}")

    def random_tour(self) -> list[int]:
        """ Generar una solucion aleatoria """

        # crear lista con tour a reordenar
        tour = list(range(self.nodos))
        # reordenar aleatoriamente el tour con la semilla
        util.random.shuffle(tour)
        # asignar que el ultimo nodo sea igual al primero
        tour.append(tour[0])

        return tour
    
    def greedy_nearest_n(self, start: int) -> list[int]:
        """ Generar una solucion del tsp usando la heuristica del nodo mas cercano comenzando del nodo start """

        tour = [0] * self.nodos
        selected = [False] * self.nodos

        # Si el nodo inicial es menor que 0
        if (start < 0):
            start = util.random.randint(0, self.nodos-1)
        tour[0] = start
        selected[start] = True

        # Ciclo para los nodos del tour
        for i in range(1,self.nodos):            
            for j in range(self.nodos):
                if (not selected[self.vecinos[tour[i-1]][j]]):
                    tour[i] = self.vecinos[tour[i-1]][j]
                    selected[self.vecinos[tour[i-1]][j]] = True
                    break
        tour.append(tour[0])
        return tour
    
    def deterministic_tour(self) -> list[int]:
        """ Generar una solucion deterministica """

        # Crear lista deterministica (rango secuencial 0 al numero de nodos)
        tour = list(range(self.nodos))
        # Retornar al inicio
        tour.append(tour[0])

        return tour
