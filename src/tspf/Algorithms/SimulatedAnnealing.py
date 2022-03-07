"""
Modulo que contiene la clase la cual representa la metaheuristica de Simulated Annealing

"""

from ..Tools import utilities, bcolors, plot, Trajectory
from . import path, csv, datetime, Path, timer, math, PrettyTable
from .. import Tour, Tsp, AlgorithmsOptions, CoolingType, InitialSolution, TSPMove

class SimulatedAnnealing():
    """ Clase Simulated Annealing la cual representa dicha metaheristica y sus metodos de búsqueda

        Parameters
        ----------
        problem : Tsp
            Instancia del problema TSP
        options : AlgorithmsOptions
            Objeto de opciones para el algoritmo

        Attributes
        ----------
        cooling : CoolingType
            Esquema de enfriamiento
        move_type : TSPMove
            Tipo de movimiento
        alpha : float
            Parametro alfa para el esquema de enfriamiento geometrico
        best_tour : Tour
            Instancia del mejor tour
        evaluations : int
            Numero de evaluaciones
        total_time : float
            Tiempo de ejecucion de Simulated Annealing
        trajectory : list
            Lista de objetos de la trayectoria de la solución

        Examples
        --------
        >>> options = AlgorithmsOptions()
        >>> problem = Tsp(filename=options.instance)
        >>> solver = SimulatedAnnealing(options=options, problem=problem)
    """
    
    def __init__(self, options: AlgorithmsOptions = None, problem: Tsp = None) -> None:

        # Atributos de instancia
        self.problem: Tsp # Problema TSP
    
        self.cooling: CoolingType # Esquema de enfriamiento
        
        self.move_type: TSPMove # Tipo de movimiento
        
        self.alpha = 0.0 # Parametro alfa para el esquema de enfriamiento geometrico
        
        self.best_tour: Tour # Mejor tour
        
        self.evaluations = 1 # numero de evaluaciones
        
        self.total_time = 0.0 # tiempo de ejecucion de Simulated Annealing

        self.options: AlgorithmsOptions # Opciones

        self.trajectory = [] # lista con la trayectoria de la solución
        
        # Si por el objeto con las opciones no es enviado al iniciar la clase
        if not options:
            self.options = AlgorithmsOptions()
        else:
            self.options = options
        # Si el objeto con el problema tsp no esta incluido
        if not problem:
            self.problem = Tsp(filename=self.options.instance)
        else:
            self.problem = problem

        self.cooling = self.options.cooling
        self.move_type = self.options.move
        self.alpha = self.options.alpha
        
        # inicializar mejor tour
        self.best_tour = Tour(problem=self.problem, type_initial_sol=InitialSolution.DETERMINISTIC)

        print(f"{bcolors.HEADER}\nIniciando Simulated Annealing...{bcolors.ENDC}")

    def print_best_solution(self) -> None:
        """ Escribir la mejor solución """
        self.updateLog()
        print()
        print(f"\t\t{bcolors.UNDERLINE}Mejor Solución Encontrada{bcolors.ENDC}\n")
        self.best_tour.printSol(True)
        print(f"{bcolors.BOLD}Total de evaluaciones:{bcolors.ENDC} {bcolors.OKBLUE}{self.evaluations-1}{bcolors.ENDC}")
        print(f"{bcolors.BOLD}Tiempo total de búsqueda con Simulated Annealing:{bcolors.ENDC} {bcolors.OKBLUE}{self.total_time:.3f} segundos{bcolors.ENDC}")

    def search(self, first_solution: Tour = None) -> None:
        """ Ejecuta la búsqueda de Simulated Annealing desde una solución inicial """

        table = PrettyTable()

        table.field_names = [f"{bcolors.BOLD}Iteraciones", "Temperatura", "Tiempo", f"Detalles{bcolors.ENDC}"]

        # Si el atributo opcional de la solución inicial no esta incluido
        if not first_solution:
            first_solution = Tour(type_initial_sol=self.options.initial_solution, problem=self.problem)

        temperature = self.options.t0 # variable de temperatura
        
        prob = 0.0 # variable para calculos de probabilidad         
 
        current_tour = Tour(tour=first_solution) # variable del tour actual 
        neighbor_tour = Tour(tour=first_solution) # variable del tour vecino generado 
        
        self.best_tour.copy(first_solution) # solución inicial se guarda como la mejor hasta el momento
        # Guardar trayectoria Inicial
        self.trajectory.append( Trajectory(
                                tour=self.best_tour.current.copy(),
                                cost=self.best_tour.cost, 
                                iterations=self.evaluations-1, 
                                evaluations=self.evaluations-1,
                                temperature=temperature) ) 
        if not self.options.replit:
            self.trajectory.append( Trajectory(
                                    tour=self.best_tour.current.copy(),
                                    cost=self.best_tour.cost, 
                                    iterations=self.evaluations-1, 
                                    evaluations=self.evaluations-1,
                                    temperature=temperature) ) 
                                
        print(f"{bcolors.UNDERLINE}\nComenzando búsqueda, solución inicial: {bcolors.ENDC}")
        self.best_tour.printSol()

        # tiempo inicial para iteraciones y condicion de termino por tiempo
        start = end = timer()
        if not self.options.silent: # si esta o no el modo silencioso que muestra los cambios en cada iteracion
            print(f"{bcolors.HEADER}\nEjecutando Simulated Annealing...\n{bcolors.ENDC}")
            #print(f"{bcolors.BOLD}\nIteracion; Temperatura; Tiempo; Detalle{bcolors.ENDC}", end='')

        # Bucle principal del algoritmo
        while (self.terminationCondition(temperature, self.evaluations, end-start)):

            details = '' # variable de texto con los detalles
            
            
            # Generar un vecino aleatoriamente a traves de un movimiento
            neighbor_tour.randomMove(self.move_type)

            # Revisar funcion objetivo de la nueva solución
            if (neighbor_tour.cost < current_tour.cost):
                # Mejor solución encontrada
                current_tour.copy(neighbor_tour)
                # Guardar trayectoria Final
                self.trajectory.append( Trajectory(
                                        tour=current_tour.current.copy(),
                                        cost=current_tour.cost, 
                                        iterations=self.evaluations, 
                                        evaluations=self.evaluations,
                                        temperature=temperature) ) 


                details += f"{bcolors.OKGREEN} Mejor costo encontrado: {current_tour.cost}{bcolors.ENDC}"

            else:
                # Calcular criterio de aceptacion
                prob = self.getAcceptanceProbability(neighbor_tour.cost, current_tour.cost, temperature)
                
                if (utilities.random.random() <= prob):
                    # Se acepta la solución peor
                    current_tour.copy(neighbor_tour)
                    
                   
                    details += f"{bcolors.FAIL} Se acepta peor costo por crit. de metrópolis: {neighbor_tour.cost}{bcolors.ENDC}"
                else:
                   # No se acepta la solución
                    details += f"{bcolors.WARNING} No se acepta peor costo por crit. de metrópolis: {neighbor_tour.cost}{bcolors.ENDC}{bcolors.OKGREEN} -> Solución actual: {current_tour.cost}{bcolors.ENDC}"

                    neighbor_tour.copy(current_tour)

			# Revisar si la nueva solución es la mejor hasta el momento
            if (current_tour.cost < self.best_tour.cost):
               
                details += f"{bcolors.OKGREEN} -> ¡Mejor solución global encontrada! {bcolors.ENDC}"

                self.best_tour.copy(current_tour)

            # Agregar la informacion a la tabla
            table.add_row([f"{bcolors.BOLD}{self.evaluations}", 
                        f"{temperature:.2f}", 
                        f"{end-start:.4f}{bcolors.ENDC}", 
                        f"{details}"
                        ])
                    
            # reducir la temperatura y aumentar las evaluaciones
            temperature = self.reduceTemperature(temperature, self.evaluations)
            self.evaluations += 1
            end = timer() # tiempo actual de iteracion

        # actualizar tiempo total de búsqueda de Simulated Annealing
        self.total_time = timer() - start
        # Guardar trayectoria Final
        self.trajectory.append( Trajectory(
                                tour=self.best_tour.current.copy(),
                                cost=self.best_tour.cost, 
                                iterations=self.evaluations-1, 
                                evaluations=self.evaluations-1,
                                temperature=temperature) ) 

        # Mostrar tabla
        if not self.options.silent:
            print(table)
            
		

    def terminationCondition(self, termperature: float, evaluations: int, time: float) -> bool:
        """ Condicion de termino para el ciclo principal de Simulated Annealing, 
        basado en los criterios de temperatura, evaluaciones y tiempo, devuelve verdadero o falso si se debe continuar o no"""
        # Criterio de termino de la temperatura
        if (self.options.tmin > 0):
            if (termperature <= self.options.tmin):
                return False
		
        # Criterio de termino de las evaluciones | iteraciones
        if (self.options.max_evaluations > 0 or self.options.max_iterations):
            if (evaluations > self.options.max_evaluations or evaluations > self.options.max_iterations):
                return False
        
        # Criterio de termino por tiempo
        if (self.options.max_time > 0):
            if (time > self.options.max_time):
                return False
        
        return True
		

    def getAcceptanceProbability (self, neighbor_cost: int, current_cost: int, temperature: float) -> float:
        """ Obtener una probabilidad aplicando el criterio de metrópolis e^-(delta/temp)"""
        # determinar delta
        delta = neighbor_cost - current_cost
        # Aplicar y retornar la formula para el criterio de metrópolis
        return math.e**-(delta / temperature) 


    def reduceTemperature(self, temperature: float, evaluation: int) -> float:
        """ Reduce la temperatura de Simulated Annealing"""
        t_new = temperature
        if (self.cooling == CoolingType.GEOMETRIC):
            t_new *= self.options.alpha
        elif (self.cooling == CoolingType.LINEAR):
            #t_new *= (1 - (evaluation / self.options.max_evaluations))
            t_new = self.options.t0 * (1 - (evaluation / self.options.max_evaluations))
        elif (self.cooling == CoolingType.LOG):
            #t_new = ((temperature * self.options.alpha) / (math.log(evaluation) + 1))
            t_new = (self.options.t0 * self.options.alpha) * (1 / (math.log(evaluation) + 1))

        return t_new

    def printSolFile(self, outputSol: str) -> None:
        """ Guarda la solución en archivo de texto"""
        utilities.printSolToFile(outputSol, self.best_tour.current)

    def printTraFile(self, outputTra: str) -> None:
        """ Guarda la trayectoria de la solución en archivo de texto"""
        utilities.printTraToFile(outputTra, self.trajectory)

    def updateLog(self) -> None:
        """ Actualiza el registro de mejores soluciones con todas las caracteristicas de su ejecución """
        # crea la carpeta en caso de que no exista (python 3.5+)
        Path("log/").mkdir(exist_ok=True)
        logFile = "log/SAlog.csv"
        # usar el archivo en modo append
        with open(logFile, "a", newline="\n") as csvfile:
            
            print(f"{bcolors.OKGREEN}\nActualizando log con mejores soluciones en archivo... {bcolors.ENDC}{path.abspath(logFile)}")
            # Headers
            fields = ["solution","cost","instance","date","alpha","t0","tmin",
                     "cooling","seed","move","max_evaluations","max_time","initial_solution"]
            writer = csv.DictWriter(csvfile, delimiter=';', fieldnames=fields)
            # Si la posicion de el archivo es cero se escriben los headers
            if not csvfile.tell():
                writer.writeheader()

            # crear texto con la solución separando cada elemento con espacios y luego guardarlo en el archivo
            sol = " ".join([str(elem) for elem in self.best_tour.current])

            # escribir la mejor solución y todas las caracteristicas de su ejecucion
            writer.writerow({
                "solution": sol, 
                "cost": self.best_tour.cost, 
                "instance": self.options.instance,
                "date": datetime.today(), 
                "alpha": self.options.alpha, 
                "t0": self.options.t0,
                "tmin": self.options.tmin, 
                "cooling": self.options.cooling.value,
                "seed": self.options.seed, 
                "move": self.options.move.value,
                "max_evaluations": self.options.max_evaluations, 
                "max_time": self.options.max_time,
                "initial_solution": self.options.initial_solution.value
            })

    def visualize(self) -> None:
        """ Visualiza la trayectoria de la solución """
        plot.Graph.replit = self.options.replit
        plot.Graph.trajectory = self.trajectory
        
        plot.show(self.options.gui)
        