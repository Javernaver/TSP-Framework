"""Modulo que contiene la clase la cual represente un recorrido para una solucion de TSP"""

from . import Tsp, InitialSolution, TSPMove, bcolors, utilities

class Tour():
    """ Clase Tour la cual representa un recorrido para una solucion de TSP, debe inicializarse obligatoriamente como diccionario

        Parameters
        ----------
        problem : Tsp
            Instancia del problema TSP
        current : list
            Recorrido actual para un tour el cual es una lista con los puntos a recorrer secuencialmente
        type_initial_sol : InitialSolution
            Tipo de solucion inicial
        tour : Tour
            Otra instancia de la misma clase

        Atributes
        ---------
        problem : Tsp
            Instancia del problema TSP
        current : list
            Recorrido actual para un tour el cual es una lista con los puntos a recorrer secuencialmente
        cost : int
            El costo o resultado de la funcion objetivo para un recorrido
        tour : Tour
            Otra instancia de la misma clase

        Examples
        --------
        >>> tour = Tour(problem=tsp_problem, type_initial_sol=InitialSolution.RANDOM)
    """
 
    def __init__(self, **kwargs) -> None:
                
        # Atributos de instancia
        self.problem: Tsp # Instancia del problema
    
        self.current = [] # Solucion actual

        self.cost = 0 # costo solucion actual

        # Si trae el problema TSP
        if ('problem' in kwargs):
            self.problem = kwargs['problem']
        
        # Tipo de solucion incial
        if ('type_initial_sol' in kwargs):
            if (kwargs['type_initial_sol'] == InitialSolution.RANDOM):
                self.current = self.problem.random_tour()
            elif (kwargs['type_initial_sol'] == InitialSolution.NEAREST_N):
                self.current = self.problem.greedy_nearest_n(-1)
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

        # Si viene la lista con el tour
        if ('current' in kwargs):
            self.current = kwargs['current'].copy()

        if (not self.problem.tsp_check_tour(self.current)):
            print(f"{bcolors.FAIL}Error: Error al inicializar la solucion inicial {bcolors.ENDC}")
            exit()

        # Determinar costo de la solucion inicial
        self.cost = self.problem.compute_tour_length(self.current)

    def copy(self, tour: 'Tour') -> None:
        """ Copia una solucion de otra instancia del objeto recibida por parametro actualizando la solucion actual """
        self.current = tour.current.copy()
        self.cost = tour.cost

    def printSol(self, final: bool = False) -> None:
        """ Escribir solucion y costo """
        self.problem.print_solution_and_cost(self.current, final)

    def printCost(self) -> None:
        """ Escribe el costo de un tour """
        print(f"Costo: {self.cost}", end='')
        
        
    """ S W A P """

    def delta_cost_swap(self, tour: list, cost: int, n1: int, n2: int) -> int:
        """ Recalcula el costo de un tour al aplicar el movimiento swap  

            Parameters
            ----------
            tour : list
                Lista del tour a modificar (sin haber sido modificado aun),
            cost : int
                El costo actual del tour
            n1, n2 : int
                Indices de los nodos para hacer swap

            Returns
            -------
            int
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
            cost = cost - self.problem.get_distance(tour[s_prev], tour[s]) \
                        - self.problem.get_distance(tour[e], tour[e_next]) \
                        + self.problem.get_distance(tour[s_prev], tour[e]) \
                        + self.problem.get_distance(tour[s], tour[e_next])
        else:
            cost = cost - self.problem.get_distance(tour[s], tour[s_next]) \
                        - self.problem.get_distance(tour[e_prev], tour[e]) \
                        + self.problem.get_distance(tour[e], tour[s_next]) \
                        + self.problem.get_distance(tour[e_prev], tour[s])
        
        if (s_next != e_next and s_next != e and s_prev != e):
            cost = cost - self.problem.get_distance(tour[s], tour[s_next]) \
                        - self.problem.get_distance(tour[e_prev], tour[e]) \
                        + self.problem.get_distance(tour[e], tour[s_next]) \
                        + self.problem.get_distance(tour[e_prev], tour[s])
        
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


    """ 2 - O P T """

    def delta_cost_two_opt(self, tour: list, cost: int, s: int, e: int) -> int:
        """ Recalcula el costo de un tour al aplicar el movimiento 2-opt    

            Parameters
            ----------
            tour : list
                Lista del tour a modificar sin haber sido modificado aun
            cost : int
                El costo actual del tour
            s, e : int
                Indices de los nodos para ser intercambiardos con 2-opt

            Returns
            -------
                int
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
        cost = cost - self.problem.get_distance(tour[s_prev], tour[s]) \
                    - self.problem.get_distance(tour[e], tour[e_next]) \
                    + self.problem.get_distance(tour[s_prev], tour[e]) \
                    + self.problem.get_distance(tour[s], tour[e_next])

        return cost
    
    def twoOptSwap(self, n1: int, n2: int) -> None:
        """ Aplica el movimiento 2-opt entre dos nodos modificando la solucion actual y su costo """
        # Si es el mismo nodo, no hay swap
        if (n1 == n2): return
        # Indice fuera de los limites
        if (n1 >= self.problem.getSize() or n2 >= self.problem.getSize()): return
        if (n1 < 0 or n2 < 0): return

        # Identificar el indice menor y el mayor
        s = min(n1, n2)
        e = max(n1, n2)
        new_tour = [] # Tour nuevo
        section = [] # seccion a aplicar 2-opt

        # Agregar la primera parte del tour no modificado por 2-opt
        new_tour = self.current[:s]

        # Extraer e invertir la seccion del tour entre [s,e] 
        section = self.current[s:e+1] # extraer
        section.reverse() # invertir
        new_tour.extend(section) # unir al nuevo tour

        # Agregar la parte final del tour no modificado por 2-opt 
        new_tour.extend(self.current[e+1:])

        # Igualar inicio y final
        new_tour[len(self.current)-1] = new_tour[0]
        
        # Actualizar costo y tour
        self.cost = self.delta_cost_two_opt(self.current, self.cost, s, e)
        self.current = new_tour.copy()


    """ 3 - O P T """
    
    def get_delta_case(self, tour: list, i: int, j: int, k: int) -> dict:
        """ Retorna un diccionario con los posibles casos para aplicar el movimiento 3-opt """
        
        a, b = tour[i], tour[i+1]
        c, d = tour[j], tour[j+1]
        e, f = tour[k], tour[k+1]

        
        deltacase = {
            1:   self.problem.get_distance(a,e) \
               + self.problem.get_distance(b,f) \
               - self.problem.get_distance(a,b) \
               - self.problem.get_distance(e,f)
               ,
            2:   self.problem.get_distance(a,c) \
               + self.problem.get_distance(b,d) \
               - self.problem.get_distance(a,b) \
               - self.problem.get_distance(c,d)
               ,

            3:   self.problem.get_distance(c,e) \
               + self.problem.get_distance(d,f) \
               - self.problem.get_distance(c,d) \
               - self.problem.get_distance(e,f)
               , 
            4:   self.problem.get_distance(a,d) \
               + self.problem.get_distance(e,c) \
               + self.problem.get_distance(b,f) \
               - self.problem.get_distance(a,b) \
               - self.problem.get_distance(c,d) \
               - self.problem.get_distance(e,f)
               , 
            5:   self.problem.get_distance(a,e) \
               + self.problem.get_distance(d,b) \
               + self.problem.get_distance(c,f) \
               - self.problem.get_distance(a,b) \
               - self.problem.get_distance(c,d) \
               - self.problem.get_distance(e,f)
               ,
            6:   self.problem.get_distance(a,c) \
               + self.problem.get_distance(b,e) \
               + self.problem.get_distance(d,f) \
               - self.problem.get_distance(a,b) \
               - self.problem.get_distance(c,d) \
               - self.problem.get_distance(e,f)
               ,
            7:   self.problem.get_distance(a,d) \
               + self.problem.get_distance(e,b) \
               + self.problem.get_distance(c,f) \
               - self.problem.get_distance(a,b) \
               - self.problem.get_distance(c,d) \
               - self.problem.get_distance(e,f)
               ,
        }
        
        return deltacase
        
    
    def delta_cost_three_opt(self, tour: list, cost: int, i: int, j: int, k: int, case: int) -> int:
        """ Recalcula el costo de un tour al aplicar el movimiento 3-opt    

            Parameters
            ----------
            tour : list
                Lista del tour a modificar sin haber sido modificado aun
            cost : int
                El costo actual del tour
            i, j, k : int
                Indices de los nodos para aplicar 3-opt

            Returns
            -------
                int
                    El nuevo costo luego de aplicar 3-opt
        """
        deltacase = self.get_delta_case(tour, i, j, k)
        cost += deltacase[case]
        return cost
         
    
    def threeOptSwap(self, i: int, j: int, k: int, case: int) -> None:
        """ Aplica el movimiento 3-opt entre dos nodos modificando la solucion actual y su costo """
        
        new_tour = []
        
        if case == 1:
            self.twoOptSwap(i, k)
        elif case == 2:
            self.twoOptSwap(i, j)
        elif case == 3:
            self.twoOptSwap(j, k)
        
        elif case == 4:
            new_tour = self.current[:i+1]
            new_tour.extend(self.current[j+1:k+1])
            new_tour.extend( reversed(self.current[i+1:j+1]) )
            new_tour.extend(self.current[k+1:])
       
        elif case == 5:
            new_tour = self.current[:i+1]
            new_tour.extend( reversed(self.current[j+1:k+1]) )
            new_tour.extend(self.current[i+1:j+1])
            new_tour.extend(self.current[k+1:])
            
        elif case == 6:
            new_tour = self.current[:i+1]
            new_tour.extend( reversed(self.current[i+1:j+1]) )
            new_tour.extend( reversed(self.current[j+1:k+1]) )
            new_tour.extend(self.current[k+1:])
            
        elif case == 7:
            new_tour = self.current[:i+1]
            new_tour.extend(self.current[j+1:k+1])
            new_tour.extend(self.current[i+1:j+1])
            new_tour.extend(self.current[k+1:])
            
        # Igualar inicio y final
        new_tour[len(self.current)-1] = new_tour[0]
            
        self.cost = self.delta_cost_three_opt(self.current, self.cost, i, j, k, case)
        self.current = new_tour.copy()


    def randomMove(self, move_type: TSPMove) -> None:
        """ Aplica un movimiento aleatorio recibido por parametro del tipo TSPMove """
        
        n1 = utilities.random.randint(0, self.problem.getSize()-1)
        n2 = utilities.random.randint(0, self.problem.getSize()-1)
        # Determinar que sean numeros diferentes
        while (n1 == n2):
            n2 = utilities.random.randint(0, self.problem.getSize()-1)

        # Seleccionar el tipo de movimiento
        if (move_type == TSPMove.TWO_OPT):
            self.twoOptSwap(n1, n2)
        elif (move_type == TSPMove.SWAP):
            self.swap(n1, n2)
        else:
            self.swap(n1, n2)


    def getPosition(self, node: int) -> int:
        """ Retorna el indice de un nodo """
        try:
            return self.current.index(node)
        except:
            return -1

    def getNode(self, pos: int) -> int:
        """ Retorna el nodo de un indice recibido """
        return self.current[pos]