""" 
Modulo que contiene la clase la cual representa el problema TSP

"""

from . import TSPlibReader
from .Tools import utilities, bcolors, plot

class Tsp():
    """
    Clase que representa el problema TSP, lee una instancia, evalua soluciones del TSP y provee metodos para crear soluciones

    Attributes
    ----------
    nodes : int
        Numero de Nodos
    distances : list[list]
        Matriz con la distacia
    neighbours : int
        Matriz con vecinos mas cercanos
    tsplib_instance : TSPlibReader
        Instancia TSP
    options : AlgorithmsOptions
        Opciones
    

    Methods
    -------
    __init__(args, opciones)
        Clase constructora, lee todas las opciones que pueda tener el problema
   
    """
    
    # errores de lectura en TSPLIB
    error = ''

    def __init__(self, filename: str) -> None:

        # Atributos de instancia
        self.instance = TSPlibReader(tsp_file_name=filename) # Instancia TSPlibReader que lee el archivo y calcula las distancias
        
        
        self.error = self.instance.error
            
        
        if not self.error:

            self.distances = self.instance.distance # Matriz con las distacias

            self.neighbours = self.instance.nn_list # Matriz con vecinos mas cercanos 
            
            self.nodes = self.instance.n # Numero de Nodos

            # Guardar coordenadas de los puntos del para generar mapeado al utilizar la graficacion
            plot.Graph.coords = self.instance.nodeptr.copy()
        
        


    def getSize(self) -> int:
        """ Obtener numero de nodos"""
        return self.nodes

    def print_distances(self) -> None:
        """ Imprimir matriz de distancia entre nodos """
        print(f"{bcolors.BOLD}Distancia entre Nodos: {bcolors.ENDC}")
        for fila in self.distances:
            for valor in fila:
                print(f"{bcolors.OKCYAN}{valor} {bcolors.ENDC}",end=" ")
            print()      

    def get_distance(self, i: int, j: int) -> int:
        """ Obtener distancia entre los nodos por su indice i y j"""
        return self.distances[i][j]

    def compute_tour_length(self, tour: list) -> int:
        """ Computar y retornar el costo de un tour """
        tour_length = 0
        for i in range(self.nodes):
            tour_length += self.distances[tour[i]][tour[i + 1]]
        return tour_length

    def tsp_check_tour(self, tour: list) -> bool:
        """ Revisa la correctitud de una solución del TSP """
        
        error = False
        used = [0] * self.nodes

        # Si no se recibio el tour 
        if (not tour):
            print(f"{bcolors.FAIL}Error: permutación no está inicializada! {bcolors.ENDC}")
            exit()

        for i in range(self.nodes):
            if used[tour[i]] != 0:
                print(f"{bcolors.FAIL}Error: la solución tiene dos veces el valor {tour[i]} (última posición: {i}) {bcolors.ENDC}")
                error = True
            else:
                used[tour[i]] = 1

        if (not error):
            for i in range(self.nodes):
                if (used[i] == 0):
                    print(f"{bcolors.FAIL}Error: posición {i} en la solución no está ocupada{bcolors.ENDC}")
                    error = True
        if (not error):
            if (tour[0] != tour[self.nodes]):
                print(f"{bcolors.FAIL}Error: la permutación no es un tour cerrado.{bcolors.ENDC}")
                error = True;
            
        if (not error):
            return True

        print(f"{bcolors.FAIL}Error: vector solución:{bcolors.ENDC} ", end='')
        for elem in tour:
            print(f"{bcolors.FAIL}{elem}{bcolors.ENDC}", end=" ")
        print()
        return False
        
    def print_solution_and_cost(self, tour: list, final: bool) -> None:
        """ Muestra la solución y costo de un tour """
        if final:
            print(f"{bcolors.BOLD}Solución Final: {bcolors.ENDC}", end='')
        else:
            print(f"{bcolors.BOLD}Solución: {bcolors.ENDC}", end='')
        for elem in tour:
            print(f"{bcolors.OKCYAN}{elem}{bcolors.ENDC}", end=' ')
        if final:
            print(f"{bcolors.BOLD}\nCosto Final: {bcolors.ENDC}{bcolors.OKCYAN}{self.compute_tour_length(tour)}{bcolors.ENDC}")
        else:
            print(f"{bcolors.BOLD}\nCosto: {bcolors.ENDC}{bcolors.OKCYAN}{self.compute_tour_length(tour)}{bcolors.ENDC}")

    def random_tour(self) -> list:
        """ Genera una solución aleatoria """
        # crear lista con tour a reordenar
        tour = list(range(self.nodes))
        # reordenar aleatoriamente el tour
        utilities.random.shuffle(tour)
        # asignar que el ultimo nodo sea igual al primero
        tour.append(tour[0])
        return tour
    
    def greedy_nearest_n(self, start: int) -> list:
        """ Genera una solución del tsp usando la heuristica del nodo mas cercano comenzando del nodo start """
        tour = [0] * self.nodes
        selected = [False] * self.nodes

        # Si el nodo inicial es menor que 0 se genera uno aleatorio para comenzar
        if (start < 0):
            start = utilities.random.randint(0, self.nodes-1)
        tour[0] = start
        selected[start] = True

        # Ciclo para los nodos del tour
        for i in range(1,self.nodes):            
            for j in range(self.nodes):
                if (not selected[self.neighbours[tour[i-1]][j]]):
                    tour[i] = self.neighbours[tour[i-1]][j]
                    selected[self.neighbours[tour[i-1]][j]] = True
                    break
        tour.append(tour[0])
        return tour
    
    def deterministic_tour(self) -> list:
        """ Genera una solución deterministica """
        # Crear lista deterministica (rango secuencial 0 al numero de nodos)
        tour = list(range(self.nodes))
        # Retornar al inicio
        tour.append(tour[0])

        return tour