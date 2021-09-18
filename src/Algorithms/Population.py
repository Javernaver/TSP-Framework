from src.Tour import Tour
from src.TSP import TSP
from typing import Union

class Population():

    # instancia del tsp
    problem: TSP
	# Poblacion
    pop = []
	# tamaño poblacion
    pop_size = 0
	# indice del mejor_individuo 
    best_index = -1
	
    def __init__(self, **kwargs) -> None:
        
        # inicializar problema
        if ('problem' in kwargs):
            self.problem = kwargs['problem']

        # Si se inicia con una poblacion
        if ('pop_size' in kwargs):
            self.pop_size = kwargs['pop_size']
            # Agregar individuos a la poblacion
            for _ in range(self.pop_size):
                self.pop.append( Tour(type_initial_sol='random', problem=self.problem) )
            # encontrar mejor individuo    
            self.searchBest()
        
        # Si se inicia con una poblacion de individos preestablecida
        if ('population' in kwargs):
            self.pop_size = len(kwargs['population']) # definir tamaño de la poblacion
            self.pop.extend(kwargs['population']) # agregar la poblacion recibida

        # Si se inicia con una poblacion general preestablecida
        if ('all' in kwargs):
            self.problem = kwargs['all'].problem # definir problema
            self.pop_size = kwargs['all'].pop_size # definir tamaño de la poblacion
            if self.pop_size > 0:
                self.pop.extend(kwargs['all'].pop) # agregar la poblacion recibida

    
    def copy(self, population: 'Population') -> None:
        """ Copia el contenido de otra instancia del objeto recibida por parametro """
        self.problem = population.problem
        self.pop_size = population.pop_size
        self.pop.clear() # limpiar lista
        # si la instancia trae una poblacion
        if self.pop_size > 0:
            self.pop.extend(population.pop)
            self.best_index = population.best_index

    
    def start(self) -> None:
        """Inicializa la poblacion"""
        self.pop.clear()
        # Agregar individuos a la poblacion
        for i in range(self.pop_size):
            self.pop.append( Tour(type_initial_sol='random', problem=self.problem) )
            self.pop[i].printSol()
        # encontrar mejor individuo    
        self.searchBest()

    
    def add(self, indivi: any) -> None:
        """Añade un individuo o varios de estos a la solucion """
        if isinstance(indivi, Tour): # si es un solo individuo
            self.pop.append(indivi)
            self.pop_size += 1
        elif isinstance(indivi, list): # si es una lista de individuos
            self.pop.extend(indivi)
            self.pop_size += len(indivi)


    def joinPopulation(self, population: 'Population') -> None:
        """Une dos poblaciones"""
        self.pop.extend(population)
        self.pop_size += population.pop_size
        self.searchBest()


    def clear(self) -> None:
        """ELimina todos los individuos de una poblacion"""
        self.pop.clear()
        self.pop_size = 0
        self.best_index = -1

    def searchBest(self) -> None:
        """ Busca el mejor individuo en la poblacion """
        # Encontrar y guardar el indice de el individuo de la poblacion con menor costo
        self.best_index = self.pop.index( min(self.pop, key=lambda tour: tour.cost) )
        
    def orderPopulation(self) -> None:
        """Ordena la poblacion de menor a mayor fitness """
        self.pop.sort(key=lambda tour: tour.cost)
        self.searchBest()