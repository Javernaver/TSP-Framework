"""Modulo que contiene la clase que representa la metaheuristica de Algoritmo Genetico"""

from . import Population, csv, datetime, Path, timer, PrettyTable
from .. import Tour, Tsp, AlgorithmsOptions, SelectionStrategy, plot, bcolors, Trajectory, utilities

class GeneticAlgorithm():
    """ Clase Simulated Annealing la cual representa dicha metaheristica y sus metodos de busqueda

        Parameters
        ----------
        problem : Tsp
            Instancia del problema TSP
        options : AlgorithmsOptions
            Objeto de opciones para el algoritmo

        Attributes
        ----------
        pop_size : int
            Numero de integrantes de la poblacion
        offspring_size : int
            Numero de hijos para los integrantes de la poblacion
        pselection_type : SelectionType
            Metodo de seleccion de padres
        crossover_type : CrossoverType
            Metodo de cruzamiento para los padres
        mutation_type : TSPMove
            Metodo de mutacion para la poblacion
        mutation_prob : float
            Probabilidad de mutacion para la poblacion
        selection_strategy : SelectionStrategy
            Estrategia de seleccion para la nueva poblacion
        gselection_type : SelectionType
            Tipo de seleccion de la poblacion
        best_tour : Tour
            Instancia del mejor tour
        evaluations : int
            Numero de evaluaciones
        iterations : int
            Numero de iteraciones
        total_time : float
            Tiempo de ejecucion de Simulated Annealing
        trajectory : list
            Lista de objetos de la trayectoria de la solucion

        Examples
        --------
        >>> options = AlgorithmsOptions()
        >>> problem = Tsp(filename=options.instance)
        >>> solver = GeneticAlgorithm(options=options, problem=problem)
    """

    def __init__(self, options: AlgorithmsOptions = None, problem: Tsp = None) -> None:

        # Atributos de instancia
        self.problem: Tsp # Problema 	

        self.best_tour: Tour = None # Mejor tour 
        
        self.total_time = 0.0 # tiempo de ejecucion de Algoritmo Genetico
        
        self.iterations = 1 # numero de iteraciones
        
        self.evaluations = 0 # numero de evaluaciones

        self.options: AlgorithmsOptions # Opciones

        self.total_time = 0.0 # tiempo de ejecucion de Algoritmo Genetico

        self.trajectory = [] # lista de listas con la trayectoria de la solucion

        # Si por el objeto con las opciones no es enviado al iniciar la clase
        if not options:
            self.options = AlgorithmsOptions()
        else:
            self.options = options
        # Si el objeto con el problema tsp no esta incluido
        if not problem:
            self.problem = Tsp(self.options.instance)
        else:
            self.problem = problem

        self.pop_size = self.options.pop_size # Parametro tamaño de la poblacion 

        self.offspring_size = self.options.offspring_size # Cantidad de hijos

        self.pselection_type = self.options.pselection_type # Seleccion de padres

        self.crossover_type = self.options.crossover_type # Cruzamiento

        self.mutation_type = self.options.mutation_type # Mutacion

        self.mutation_prob = self.options.mutation_prob # Probabilidad de mutacion

        self.selection_strategy = self.options.selection_strategy # Estrategia de seleccion de la nueva poblacion

        self.gselection_type = self.options.gselection_type # Tipo de seleccion de la poblacion

        print(f"{bcolors.HEADER}\nIniciando Algortimo Genetico...{bcolors.ENDC}")


    def print_best_solution(self) -> None:
        """ Escribir la mejor solucion """
        print()
        print(f"\t\t{bcolors.UNDERLINE}Mejor Solucion Encontrada{bcolors.ENDC}\n")
        self.best_tour.printSol(True)
        print(f"{bcolors.BOLD}Total de iteraciones:{bcolors.ENDC} {bcolors.OKBLUE}{self.iterations-1}{bcolors.ENDC}")
        print(f"{bcolors.BOLD}Total de evaluaciones:{bcolors.ENDC} {bcolors.OKBLUE}{self.evaluations-self.offspring_size}{bcolors.ENDC}")
        print(f"{bcolors.BOLD}Tiempo total de busqueda con Algoritmo Genetico:{bcolors.ENDC} {bcolors.OKBLUE}{self.total_time:.3f} segundos{bcolors.ENDC}")
        self.updateLog()


    def search(self) -> None:
        """ Ejecuta la busqueda del Algoritmo Genetico desde una poblacion generada aleatoriamente """

        # Tabla para almacenar la informacion de la ejecucion
        table = PrettyTable()
        # cabezeras de la tabla
        table.field_names = [f"{bcolors.BOLD}Iteraciones", "Evaluaciones", "Tiempo", "Minimo",
        "Promedio", "Desv. Estandar", f"Detalles{bcolors.ENDC}"]
        
        parents = []
        # Inicializar poblacion
        print(f"{bcolors.BOLD}Generando poblacion inicial...{bcolors.ENDC}")
        population = Population(pop_size=self.pop_size, problem=self.problem)
        # Iniciar poblacion de hijos
        offspring = Population(problem=self.problem)
        #population.printPop()

        # Imprimir mejor solución encontrada 
        print(f"{bcolors.UNDERLINE}Mejor individuo de la poblacion{bcolors.ENDC}")
        population.getBestTour().printSol()
        
        # Guardar la mejor solucion en best_tour
        if not self.best_tour:
            self.best_tour = Tour(tour=population.getBestTour())
        else:
            self.best_tour.copy(population.getBestTour())
        
        # Guardar trayectoria
        self.trajectory.append( Trajectory(self.best_tour.current.copy(),
                                self.best_tour.cost, 0, self.evaluations,
                                population.getAverage(), population.getDeviation()) ) 
        self.evaluations += self.offspring_size

        # tiempo para iteraciones y condicion de termino por tiempo
        start = end = timer()
        if not self.options.silent: # si esta o no el modo silencioso que muestra los cambios en cada iteracion
            print(f"{bcolors.HEADER}\nEjecutando Algoritmo Genetico...\n{bcolors.ENDC}")


        # Bucle principal del algoritmo
        while (self.terminationCondition(self.iterations, self.evaluations, end-start)):

            details = '' # variable de texto con los detalles 
               
            # Aplicar cruzamiento para generar poblacion de hijos
            while (offspring.pop_size < self.offspring_size):
                parents = population.selectParents(self.pselection_type)
                offspring.add( population.crossover(parents, self.crossover_type) )
            
            # Aplicar mutacion
            offspring.mutation(self.mutation_prob, self.mutation_type)
             
            # Revisar si algun hijo es la mejor solucion hasta el momento
            if (offspring.getBestTour().cost < self.best_tour.cost):
        
                details = f"{bcolors.OKGREEN} Mejor actual: {self.best_tour.cost} -> {offspring.getBestTour().cost} ¡Actualizado!{bcolors.ENDC}"
                    
                self.best_tour.copy(offspring.getBestTour())
                # Guardar trayectoria
                self.trajectory.append( Trajectory(self.best_tour.current.copy(),
                                        self.best_tour.cost, self.iterations, self.evaluations,
                                        population.getAverage(), population.getDeviation()) ) 
                
            else: 
                details = f"{bcolors.OKBLUE} Mejor actual: {self.best_tour.cost}{bcolors.ENDC}"

            # Agregar la informacion de la iteracion a la tabla la tabla
            table.add_row([f"{bcolors.BOLD}{self.iterations}", 
                        f"{self.evaluations}", 
                        f"{end-start:.4f}", 
                        f"{offspring.getBestTour().cost}", 
                        f"{offspring.getAverage():.2f}", 
                        f"{offspring.getDeviation():.2f}{bcolors.ENDC}", 
                        f"{details}"
                        ])

            # Seleccionar nueva poblacion
            if (self.selection_strategy == SelectionStrategy.MULAMBDA):
                # Seleccionar solo desde los hijos
                if (self.offspring_size > self.pop_size):
                    # Seleccionar desde los hijos
                    offspring.selectPopulation(self.pop_size, self.gselection_type)
                
                population.copy(offspring)
            elif (self.selection_strategy == SelectionStrategy.MUPLUSLAMBDA):
                # Seleccionar desde los hijos y los padres
                # Unir ambas poblaciones (hijos y padres)
                offspring.joinPopulation(population)
                # Seleccionar desde estas poblaciones
                offspring.selectPopulation(self.pop_size, self.gselection_type)
                population.copy(offspring)            
                    
            # Actualizar contadores de iteraciones y evaluaciones, luego limpiar la poblacion de hijos
            self.evaluations += self.offspring_size
            self.iterations += 1
            offspring.clear()
            end = timer() # tiempo actual de iteracion

        # Mostrar la tabla con toda la informacion de la ejecucion del algoritmo
        if not self.options.silent:
            print(table)
            #text = table.get_csv_string(delimiter=';')
            #print(text)

        # actualizar tiempo total de busqueda de Algoritmo Genetico
        self.total_time = timer() - start


    def terminationCondition(self, iterations: int, evaluations: int, time: float) -> bool:
        """ Condicion de termino para el ciclo principal de Algoritmo Genetico, 
        basado en los criterios de iteraciones, evaluaciones y tiempo, devuelve verdadero o falso si se debe continuar o no"""
        
        # Criterio de termino de las iteraciones
        if (self.options.max_iterations > 0):
            if (iterations > self.options.max_iterations):
                return False
        # Criterio de termino de las evaluciones
        if (self.options.max_evaluations > 0):
            if (evaluations > self.options.max_evaluations):
                return False
        # Criterio de termino por tiempo
        if (self.options.max_time > 0):
            if (time > self.options.max_time):
                return False
        
        return True

    def printSolFile(self, outputSol: str) -> None:
        """ Guarda la solucion en archivo de texto"""
        utilities.printSolToFile(outputSol, self.best_tour.current)

    def printTraFile(self, outputTra: str) -> None:
        """ Guarda la trayectoria de la solucion en archivo de texto"""
        utilities.printTraToFile(outputTra, self.trajectory)

    def updateLog(self) -> None:
        """ Actualiza el registro de mejores soluciones con todas las caracteristicas de su ejecución """
        # crea la carpeta en caso de que no exista (python 3.5+)
        Path("log/").mkdir(exist_ok=True)
        # usar el archivo en modo append
        with open("log/GAlog.csv", "a", newline="\n") as csvfile:
            
            # Headers
            fields = ["solution","cost","instance","date","pop_size","offspring_size", 
                     "pselection_type","crossover_type","mutation_type","mutation_prob", 
                     "selection_strategy","gselection_type","seed","move","max_evaluations",
                     "max_iterations","max_time","initial_solution"]

            writer = csv.DictWriter(csvfile, delimiter=';', fieldnames=fields)
            # Si la posicion de el archivo es cero se escriben los headers
            if not csvfile.tell():
                writer.writeheader()

            # crear texto con la solucion separando cada elemento con espacios y luego guardarlo en el archivo
            sol = " ".join([str(elem) for elem in self.best_tour.current])

            # escribir la mejor solucion y todas las caracteristicas de su ejecucion
            writer.writerow({
                "solution": sol, 
                "cost": self.best_tour.cost, 
                "instance": self.options.instance, 
                "date": datetime.today(), 
                "pop_size": self.options.pop_size, 
                "offspring_size": self.options.offspring_size, 
                "pselection_type": self.options.pselection_type.value, 
                "crossover_type": self.options.crossover_type.value, 
                "mutation_type": self.options.mutation_type.value,
                "mutation_prob": self.options.mutation_prob, 
                "selection_strategy": self.options.selection_strategy.value, 
                "gselection_type": self.options.gselection_type.value, 
                "seed": self.options.seed, 
                "move": self.options.move.value, 
                "max_evaluations": self.options.max_evaluations,
                "max_iterations": self.options.max_iterations, 
                "max_time": self.options.max_time,
                "initial_solution": self.options.initial_solution.value
            })
    

    def visualize(self, replit: bool) -> None:
        """ Visualiza la trayectoria de la solucion"""
        plot.replit = replit
        plot.trajectory = self.trajectory
        plot.show()
        