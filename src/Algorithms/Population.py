from src.Tour import Tour
from src.TSP import TSP


class Population():

    # instancia del tsp
    problem :TSP
	# Poblacion
    pop = []
	# tamaño poblacion
    pop_size = 0
	# indice del mejor_individuo 
    best_index = 0
	
    def __init__(self, **kwargs) -> None:
        
        if ('problem' in kwargs):
            self.problem = kwargs['problem']
        if ('pop_size' in kwargs):
            self.pop_size = kwargs['pop_size']
        self.best_index = -1

        for _ in range(self.pop_size):
            self.pop.append( Tour(type_initial_sol='random', problem=self.problem) )

        self.searchBest()

   
    def searchBest(self) -> None:
        """ Busca el mejor individuo en la poblacion """
        # Encontrar y guardar el indice de el individuo de la poblacion con menor costo
        self.best_index = self.pop.index( min(self.pop, key=lambda tour: tour.cost) )
        
 