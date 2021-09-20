from src.AlgorithmsOptions import SelectionType
from src.Utilities import bcolors, random
from src.Tour import Tour
from src.TSP import TSP

class Population():

    
    def __init__(self, **kwargs) -> None:

        # instancia del tsp
        self.problem: TSP
        # Poblacion
        self.pop = []
        # tamaño poblacion
        self.pop_size = 0
        # indice del mejor_individuo 
        self.best_index = -1


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
            print(self.best_index, len(self.pop), indivi)
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
        if self.pop:
            self.best_index = self.pop.index( min(self.pop, key=lambda tour: tour.cost) )


    def orderPopulation(self) -> None:
        """Ordena la poblacion de menor a mayor fitness """
        self.pop.sort(key=lambda tour: tour.cost)
        self.searchBest()

    
    # Impresiones
    def printPop(self) -> None:
        """Imprime la poblacion de soluciones i costo"""
        for i in range(self.pop_size):
            print(f"{bcolors.UNDERLINE}Individuo {i+1}{bcolors.ENDC}")
            self.pop[i].printSol()

    """ METODOS VARIOS """

    def getBestTour(self) -> Tour:
        """Retorna el mejor individuo de la poblacion"""
        if (self.best_index > -1):
            return self.pop[self.best_index]
        return None

    def generateRouletteWheel(self, candidates: list) -> list:
        """ Retorna la torta de probabilidades asociadas al fitness de las soluciones entregadas, la seleccion es 
        proporcional al fitness
        Ruleta para minimizacion: p(x1) = (min + max - f(x1)) / sum(f(x))

        Returns
        -------
            list[float]
                lista que posee las probabilidades acumuladas para la seleccion de soluciones
        """
        su = 0.0
        # Encontrar el minimo y el máximo en los individuos
        mini = (min(candidates, key=lambda tour: tour.cost)).cost
        maxi = (max(candidates, key=lambda tour: tour.cost)).cost
        roulette = [0.0] * len(candidates)

        # Generar ruleta
        for i in range(len(candidates)):
            roulette[i] = float(mini + maxi - candidates[i].cost)
            su += roulette[i]

        roulette[0] /= su
        for i in range(1, len(candidates)):
            roulette[i] /= su
            roulette[i] += roulette[i-1]

        return roulette


    """ METODOS DE SELECCION DE PADRES (2) """

    def selectParents(self, stype: SelectionType) -> list:
        """ Selecciona 2 padres segun el tipo de seleccion recibido por parametro 
         
            Returns
            -------
            list[int]
                lista con los indices de los padres seleccionados
        """
        parents = []

        if (stype == SelectionType.BEST):
            parents = self.selectIBest(2)
        elif (stype == SelectionType.RANDOM):
            parents = self.selectIRandom(2)
        elif (stype == SelectionType.ROULETTE):
            parents = self.selectIRoulette()
        elif (stype == SelectionType.TOURNAMENT):
            parents = self.selectITournament()
        else: 
            parents = self.selectIBest(2)
        
        return parents

    def selectIBest(self, size: int = 2) -> list:
        """Selecciona la cantidad de individuos recibida por parametros (por defecto 2) en base al fitness, siendo una seleccion elitista
            
            Returns
            -------
            list
                lista con los indices de los individuos seleccionados
        """
        sel = []
        # Si se seleccionan mas individuos de los permitidos
        if (size > self.pop_size):
            print(f"{bcolors.FAIL}Error: No es posible seleccionar {size} de una poblacion con {self.pop_size} individuos{bcolors.ENDC}")
            exit()
 
        # Si todos son seleccionados
        if (size == self.pop_size):
            sel = list(range(size))
            return sel
        
        # Ordenar poblacion
        self.orderPopulation()
        # Seleccionar
        sel = list(range(size))

        return sel

    
    def selectIRandom(self, size: int = 2) -> list:
        """Selecciona individuos aleatoriamente (por defecto 2)
         
            Returns
            -------
            list
                lista con los indices de los individuos seleccionados
        """
        sel = [] 
        elegible = []
        # Si se seleccionan mas individuos de los permitidos
        if (size > self.pop_size):
            print(f"{bcolors.FAIL}Error: No es posible seleccionar {size} de una poblacion con {self.pop_size} individuos{bcolors.ENDC}")
            exit()
        
        # Si todos son seleccionados
        if (size == self.pop_size):
            sel = list(range(size))
            return sel

        # Indices de los candidatos que pueden ser seleccionados
        elegible = list(range(self.pop_size))
        # Seleccionar los individuos aleatoriamente desde los candidatos y del tamaño recibido
        sel = random.sample(elegible, size)

        return sel

    def selectIRoulette(self, size: int = 2) -> list:
        """Selecciona los individuos padres en base a la ruleta (por defecto 2)

            Returns
            -------
            list
                lista con los indices de los individuos seleccionados
        """
        candidates = []
        ids = []
        sel = []
        roulette = []
        r = 0.0

        # Si se seleccionan mas individuos de los permitidos
        if (size > self.pop_size):
            print(f"{bcolors.FAIL}Error: No es posible seleccionar {size} de una poblacion con {self.pop_size} individuos{bcolors.ENDC}")
            exit()
        
        # Si todos son seleccionados
        if (size == self.pop_size):
            sel = list(range(size))
            return sel
        # Anadir candidatos a ser seleccionados y sus ids
        candidates.extend(self.pop)
        ids = list(range(len(self.pop)))

        # Seleccionar individuos
        for _ in range(size):
            # Generar ruleta
            roulette = self.generateRouletteWheel(candidates)
            # Seleccionar
            r = random.random()
            for i in range(len(candidates)):
                if (r < roulette[i]):
                    sel.append(ids[i])
                    candidates.pop(i)
                    ids.pop(i)
                    break

        return sel

    def selectITournament(self, tsize: int = 3, size: int = 2) -> list:
        """Selecciona individuos en base al fitness (por defecto 2) en un torneo (por defecto 3 participantes)

            Returns
            -------
            list
                lista con los indices de los individuos seleccionados
        """
        sel = []
        tsel = []
        # Si se seleccionan mas individuos de los permitidos
        if (size > self.pop_size):
            print(f"{bcolors.FAIL}Error: No es posible seleccionar {size} de una poblacion con {self.pop_size} individuos{bcolors.ENDC}")
            exit()
        
        # reducir el tamaño del torneo si es necesario
        while (tsize > self.pop_size):
            tsize -= 1
    	
        # Si todos son seleccionados
        if (size == self.pop_size):
            sel = list(range(size))
            return sel

        # Seleccionar individuos
        while (len(sel) < size):
            # seleccionar individuos torneo
            tsel = self.selectIRandom(tsize)

            # Seleccionar y añadir mejor individuo de los individuos aleatorios del torneo
            sel.append( min(tsel, key=lambda i: self.pop[i].cost) )
            # convertir a set y luego a lista nuevamente para eliminar en caso de que hallan elementos repetidos
            sel = list( set(sel) )
            
        return sel
    	
  