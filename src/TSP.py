from src.Utilities import bcolors
from src.TSPlibReader import TSPlibReader
from src import Utilities
from functools import reduce

class TSP():

    # Numero de Nodos
    nodos = 0

    # Matriz con la distacia 
    distancia = [[]]

    # Matriz con vecinos mas cercanos 
    nn_list = [[]]

    # Instancia TSP
    tsplib_instance = None

    def __init__(self, instance) -> None:
        
        # leer instancia desde un archivo TSPlib
        self.tsplib_instance = TSPlibReader(instance)

        # obtener matriz de distancia
        self.distancia = self.tsplib_instance.distance
        # obtener vecinos mas cercanos
        self.nn_list = self.tsplib_instance.nn_list
        
        # obtener tamano de la instancia 
        self.nodos = self.tsplib_instance.n

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

    def get_distance (self, i, j) -> list[list]:
        """ Obtener distancia entre los nodos por su indice i y j"""
        return self.distancia[i][j]

    def compute_tour_length(self, tour) -> int:
        """ Computar y retornar el costo de un tour """
        return 0

    def tsp_check_tour(tour) -> bool:
        """ Revisa la correctitud de una solucion del TSP """
        pass

  