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
        print(self.compute_tour_length([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 11, 13, 0]))
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

    def get_distance(self, i, j) -> list[list]:
        """ Obtener distancia entre los nodos por su indice i y j"""
        return self.distancia[i][j]

    def compute_tour_length(self, tour) -> int:
        """ Computar y retornar el costo de un tour """
        tour_length = 0
        for i in range(self.nodos):
            tour_length += self.distancia[tour[i]][tour[i + 1]]
        return tour_length

    def tsp_check_tour(self, tour) -> bool:
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
        