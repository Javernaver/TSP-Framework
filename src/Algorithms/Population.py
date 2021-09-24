from src.AlgorithmsOptions import CrossoverType, MutationType, SelectionType
from src.Utilities import bcolors, random
from src.Tour import Tour
from src.TSP import TSP

class Population():

    
    def __init__(self, **kwargs) -> None:

        # Instancia del problema TSP
        self.problem: TSP
        # Poblacion
        self.pop = []
        # Tamaño de la poblacion
        self.pop_size = 0
        # Indice del mejor individuo 
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

    def getIndividuals(self, index: list) -> list:
        """Retorna individuos segun una lista con indices

            Parameters
            ----------
            index : list
                lista con los indices de los individuos
         
            Returns
            -------
            list
                lista con los individuos requeridos
        """
        selected = []
        for i in range(len(index)):
            selected.append(self.pop[index[i]])

        return selected

    def generateRouletteWheel(self, candidates: list) -> list:
        """ Retorna la torta de probabilidades asociadas al fitness de las soluciones entregadas, la seleccion es 
        proporcional al fitness
        Ruleta para minimizacion: p(x1) = (min + max - f(x1)) / sum(f(x))

        Parameters
        ----------
        candidates : list
            lista con los candidatos que participan de la ruleta 

        Returns
        -------
            list
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
        """ Selecciona 2 padres segun el tipo de seleccion

            Parameters
            ----------
            stype : SelectionType
                tipo de seleccion
         
            Returns
            -------
            list
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
        """Selecciona la cantidad de individuos recibida por parametros en base al fitness, siendo una seleccion elitista

            Parameters
            ----------
            size : int, optional
                tamaño de individuos a seleccionar (por defecto 2)
            
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
        """Selecciona individuos aleatoriamente

            Parameters
            ----------
            size : int, optional
                tamaño de individuos a seleccionar (por defecto 2)

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
        """Selecciona los individuos padres en base a la ruleta

            Parameters
            ----------
            size : int, optional
                tamaño de individuos a seleccionar (por defecto 2)

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
        ids = list(range(len(candidates)))

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
        """Selecciona individuos en base al fitness en un torneo

            Parameters
            ----------
            tsize : int, optional
                tamaño de los participantes del torneo (por defecto 3)
            size : int, optional
                tamaño de los individuos seleccionados o ganadores del torneo (por defecto 2)

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
    	
    
    """ METODOS DE CRUZAMIENTO """

    def crossover(self, parents_id: list, ctype: CrossoverType) -> list:
        """Aplica el operador cruzamiento

            Parameters
            ----------
            parents_id : list
                lista con los indices de los individuos padres seleccionados para cruzamiento
            ctype : CrossoverType
                tipo de cruzamiento

            Returns
            -------
            list
                lista con los individuos hijos generados

        """
        offspring = []
        parents = []
        # Obtener indivuduos padres con los ids
        parents.extend( self.getIndividuals(parents_id) )

        # Aplicar Crossover
        if (ctype == CrossoverType.PMX):
            offspring.extend( self.PMXCrossover(parents) )
        elif (ctype == CrossoverType.OX):
            offspring.extend( self.OXCrossover(parents) )
        elif (ctype == CrossoverType.OPX):
            offspring.extend( self.OPXCrossover(parents) )
        else:
            offspring.extend( self.OXCrossover(parents) )

        return offspring


    def PMXCrossover(self, parents: list) -> list:
        """Aplica el operador PMX a los padres

            Parameters
            ----------
            parents : list
                lista con los 2 individuos padres seleccionados para cruzamiento

            Returns
            -------
            list
                lista con los 2 hijos resultantes del cruzamiento
        """
        size = self.problem.getSize() # tamaño del tour
        offspring = []
        p1 = parents[0] # padre 1
        p2 = parents[1] # padre 2
        o1 = Tour(tour=p1) # hijo 1
        o2 = Tour(tour=p2) # hijo 2

        cpoint = 0 # punto de cruzamiento
        aux = 0
        # Obtener punto de crossover aleatoriamente
        cpoint = random.randint(0, size-1)
        # Generar el primer hijo
        for i in range(cpoint):
            aux = o1.getPosition( p2.getNode(i) )
            o1.swap(i, aux)

        # Generar el segundo hijo
        for i in range(cpoint, size):
            aux = o2.getPosition( p1.getNode(i) )
            o2.swap(i, aux)

        offspring.append(o1)
        offspring.append(o2)
        return offspring
    	

    def OXCrossover(self, parents: list) -> list:
        """Aplica el operador OX a los padres

            Parameters
            ----------
            parents : list
                lista con los 2 individuos padres seleccionados para cruzamiento

            Returns
            -------
            list
                lista con los 2 hijos resultantes del cruzamiento
        """
        size = self.problem.getSize() # tamaño del tour
        p1 = parents[0] # padre 1
        p2 = parents[1] # padre 2
        aux1in = [] # auxiliar para las seccion extraida del padre 1
        aux1out = [] # auxiliar para las seccion no extraida desde el padre 2 al hijo 1
        aux2in = [] # auxiliar para las seccion extraida del padre 2
        aux2out = [] # auxiliar para las seccion no extraida desde el padre 1 al hijo 2
        h1 = [] # hijo 1
        h2 = [] # hijo 2
        offspring = [] # lista para almacenar los hijos

        # Generar numeros aleatorios con los limites para las secciones del cruzamiento 
        r1 = random.randint(0, size-1)
        r2 = random.randint(0, size-1)
        while (r1 >= r2): # repetir hasta que el limite 2 sea mayor que el limite 1
            r1 = random.randint(0, size-1)
            r2 = random.randint(0, size-1)
        
        # Guardar los rangos de secciones de los padres segun los indices generados guardandolos en listas auxiliares
        aux1in = p1.current[r1:r2] 
        aux2in = p2.current[r1:r2]

        # Guardar los elementos distintos que no se quitaron del padre 2 al hijo 1 y vice versa 
        for i in range(size):
            if not p2.getNode(i) in aux1in:
                aux1out.append( p2.getNode(i) )
            if not p1.getNode(i) in aux2in:
                aux2out.append( p1.getNode(i) )
            
        #print(p2.current, p1.current)
        #print(aux1in, len(aux1in), aux1out, len(aux1out), aux2in, len(aux2in), aux2out, len(aux2out))

        # Añadir y eliminar desde las listas con los elementos no extraidos a los hijos que se generaran la cantidad de veces donde comienzan estas
        for _ in range(r1):
            h1.append(aux1out[0])
            aux1out.pop(0)
            h2.append(aux2out[0])
            aux2out.pop(0)       
       
        # Añadir a los hijos las secciones extraidas de los padres
        h1.extend(aux1in)
        h2.extend(aux2in)

        # Añadir el resto de las listas con los elementos no extraidos a los hijos que se generaran 
        h1.extend(aux1out)
        h2.extend(aux2out)
       
        
        # Completar las rutas para que se vuelva al comienzo y concretar el tour
        h1.append(h1[0])
        h2.append(h2[0])
        # Guardar los hijos como lista de tours
        offspring.append( Tour(current=h1, problem=self.problem) )
        offspring.append( Tour(current=h2, problem=self.problem) )

        #print( r1, r2 , h1 , len(h1), h2, len(h2))
        return offspring

    def OPXCrossover(self, parents: list) -> list:
        """Aplica el operador OPX o cruzamiento en un punto a los padres.

            Parameters
            ----------
            parents : list
                lista con los 2 individuos padres seleccionados para cruzamiento

            Returns
            -------
            list
                lista con los 2 hijos resultantes del cruzamiento
        """
        size = self.problem.getSize() # tamaño del tour
        p1 = parents[0] # padre 1
        p2 = parents[1] # padre 2
        h1 = [] # hijo 1
        h2 = [] # hijo 2
        aux1in = [] # auxiliar para las seccion extraida del padre 1
        aux1out = [] # auxiliar para las seccion no extraida desde el padre 2 al hijo 1
        aux2in = [] # auxiliar para las seccion extraida del padre 2
        aux2out = [] # auxiliar para las seccion no extraida desde el padre 1 al hijo 2
        offspring = [] # lista para almacenar los hijos
        cpoint = 0 # punto de cruzamiento

        # Generar punto de cruzamiento
        cpoint = random.randint(0, size-1)
        # Guardar los rangos desde el punto de cruzamiento del padre 2 al hijo 1 y del padre 1 al hijo 2
        aux1in = p2.current[cpoint:] 
        aux1in.pop() # eliminar el ultimo nodo que es igual al inicial del tour
        aux2in = p1.current[cpoint:]
        aux2in.pop() # eliminar el ultimo nodo que es igual al inicial del tour

        # Guardar los elementos distintos que no se quitaron del padre 1 al hijo 1 y del padre 2 al hijo 2
        for i in range(size):
            if not p1.getNode(i) in aux1in:
                aux1out.append( p1.getNode(i) )
            if not p2.getNode(i) in aux2in:
                aux2out.append( p2.getNode(i) )
        
        # Agregar los elementos distintos que se encontraron despues de la extraccion de la seccion de cruzamiento
        h1.extend(aux1out)           
        h2.extend(aux2out)
        
        # Agregar los elementos extraidos del cruzamiento
        h1.extend(aux1in)
        h2.extend(aux2in)
        
        # Completar las rutas para que se vuelva al comienzo y concretar el tour
        h1.append(h1[0])
        h2.append(h2[0])
        # Guardar los hijos como lista de tours
        offspring.append( Tour(current=h1, problem=self.problem) )
        offspring.append( Tour(current=h2, problem=self.problem) )
        
        #print(p1.current, p2.current, cpoint)
        #print(h1, len(h1), h2, len(h2))
        return offspring


    """ METODOS DE MUTACION """

    def mutation(self, mut_probability: float, mtype: MutationType) -> None:
        """ Aplica el operador de mutacion

            Parameters
            ----------
            mut_probability : float
                probabilidad de mutacion 
            mtype : MutationType
                tipo de mutacion 
        """
        if (mtype == MutationType.SWAP):
            self.swapMutation(mut_probability)
        elif (mtype == MutationType.TWO_OPT):
            self.twoOptMutation(mut_probability)
        else:
            self.swapMutation(mut_probability)

        self.searchBest()


    def swapMutation(self, mut_probability: float) -> None:
        """Aplica swap aleatoriamente a toda la poblacion segun la probabilidad recibida

            Parameters
            ----------
            mut_probability : float
                probabilidad de mutacion
        """
        r = 0.0
        for i in range(self.pop_size):
            # obtener probabilidad de [0,1]
            r = random.random()
            if (mut_probability > r):
                self.pop[i].randomSwap()  

    def twoOptMutation(self, mut_probability: float) -> None:
        """Aplica el movimiento 2opt aleatoriamente a toda la poblacion segun la probabilidad recibida

            Parameters
            ----------
            mut_probability : float
                probabilidad de mutacion
        """
        r = 0.0
        for i in range(self.pop_size):
            # obtener probabilidad de [0,1]
            r = random.random()
            if (mut_probability > r):
                self.pop[i].randomTwoOptSwap()
