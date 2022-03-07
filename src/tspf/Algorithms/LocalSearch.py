"""
Modulo que contiene la clase la cual representa el metodo de búsqueda de LocalSearch

"""

from ..Tools import utilities, bcolors, plot, Trajectory
from . import path, csv, datetime, Path, timer, PrettyTable
from .. import AlgorithmsOptions, Tsp, Tour, TSPMove, InitialSolution

class LocalSearch():
    
    
    def __init__(self, options: AlgorithmsOptions = None, problem: Tsp = None) -> None:
        """ Clase Local Search la cual representa este metodo de búsqueda

        Parameters
        ----------
        problem : Tsp
            Instancia del problema TSP
        options : AlgorithmsOptions
            Objeto de opciones para el algoritmo

        Attributes
        ----------
        move_type: TSPMove
            Tipo de movimiento
        best_tour : Tour
            Instancia del mejor tour
        evaluations : int
            Numero de evaluaciones
        total_time : float
            Tiempo de ejecucion de Local Search
        trajectory : list
            Lista de objetos de la trayectoria de la solución
        bestImprovement : bool
            Si es de tipo best improvement o no

        Examples
        --------
        >>> options = AlgorithmsOptions()
        >>> problem = Tsp(filename=options.instance)
        >>> solver = LocalSearch(options=options, problem=problem)
    """

        # Atributos de instancia
        self.problem: Tsp # Problema TSP
        
        self.move_type: TSPMove # Tipo de movimiento
        
        self.best_tour: Tour # Mejor tour
        
        self.evaluations = 1 # numero de evaluaciones
        
        self.total_time = 0.0 # tiempo de ejecucion de Simulated Annealing

        self.options: AlgorithmsOptions # Opciones

        self.trajectory = [] # lista con la trayectoria de la solución
        
        self.bestImprovement = False # si es best improvement
        
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

        self.move_type = options.move
        self.bestImprovement = options.bestImprovement
        
        # inicializar mejor tour
        self.best_tour = Tour(problem=self.problem, type_initial_sol=InitialSolution.RANDOM)
        
        
    def print_best_solution(self) -> None:
        """ Escribir la mejor solución """
        self.updateLog()
        print()
        print(f"\t\t{bcolors.UNDERLINE}Mejor Solución Encontrada{bcolors.ENDC}\n")
        self.best_tour.printSol(True)
        print(f"{bcolors.BOLD}Total de evaluaciones:{bcolors.ENDC} {bcolors.OKBLUE}{self.evaluations-1}{bcolors.ENDC}")
        print(f"{bcolors.BOLD}Tiempo total de búsqueda con Local Search:{bcolors.ENDC} {bcolors.OKBLUE}{self.total_time:.3f} segundos{bcolors.ENDC}")

    
    def search(self, first_solution: Tour = None) -> None:
        """ Ejecuta la búsqueda de Local Search desde una solución inicial """

        table = PrettyTable()

        table.field_names = [f"{bcolors.BOLD}Evaluaciones", "Tiempo", f"Detalles{bcolors.ENDC}"]

        # Si el atributo opcional de la solución inicial no esta incluido
        if not first_solution:
            first_solution = Tour(type_initial_sol=self.options.initial_solution, problem=self.problem)

 
        current_tour = Tour(tour=first_solution) # variable del tour actual
        
        self.best_tour.copy(first_solution) # solución inicial se guarda como la mejor hasta el momento
        # Guardar trayectoria Inicial
        self.trajectory.append( Trajectory(
                                tour=self.best_tour.current.copy(),
                                cost=self.best_tour.cost, 
                                iterations=self.evaluations-1, 
                                evaluations=self.evaluations-1) )
        if not self.options.replit:
            self.trajectory.append( Trajectory(
                                    tour=self.best_tour.current.copy(),
                                    cost=self.best_tour.cost, 
                                    iterations=self.evaluations-1, 
                                    evaluations=self.evaluations-1) )
                                
        print(f"{bcolors.UNDERLINE}\nComenzando búsqueda, solución inicial: {bcolors.ENDC}")
        self.best_tour.printSol()

       
        if not self.options.silent: # si esta o no el modo silencioso que muestra los cambios en cada iteracion
            print(f"{bcolors.HEADER}\nEjecutando Local Search...\n{bcolors.ENDC}")
            
            
        # Ejecucion de la búsqueda segun el metodo
        if self.move_type == TSPMove.SWAP:
            self.swapSearch(current_tour, table)
        elif self.move_type == TSPMove.TWO_OPT:
            self.twoOptSearch(current_tour, table)
        elif self.move_type == TSPMove.THREE_OPT:
            self.threeOptSearch(current_tour, table)
        else:
            self.twoOptSearch(current_tour, table)
        

        # Mostrar tabla
        if not self.options.silent:
            print(table)
            #print()
            
        # Guardar Trayectoria Final
        self.trajectory.append( Trajectory(
                            tour=current_tour.current.copy(),
                            cost=current_tour.cost, 
                            iterations=self.evaluations, 
                            evaluations=self.evaluations) )

    """
    
    
    S W A P
    
    
    """
            
    def swapSearch(self, tour: Tour, table: PrettyTable = PrettyTable()) -> None:
        """ Aplica la búsqueda por 3-opt """
        #print(tour.current)   
        n = self.problem.getSize()
        if n < 3: 
            return
        
        # tiempo inicial para iteraciones y condicion de termino por tiempo
        start = end = timer()
        a, b = 0, 0 # indices auxiliares
        improved = True
        best_cost = self.best_tour.cost # mejor optimo local
        
        while improved:
            
            details = '' # variable de texto con los detalles

            improved = False
            
            for i in range(n):
                if improved and not self.bestImprovement: # si es best improvement se continua el loop si no se corta al ser first improvement
                    break
                for j in range(i + 1, n):
                    if improved and not self.bestImprovement:
                        break
                    
                    if tour.delta_cost_swap(tour.current, tour.cost, i, j) < best_cost:
                        
                        a, b = i, j # se guardan los indices del optimo local si se encuentra uno mejor
                        
                        if self.bestImprovement: # cuando sea best improvement se sigue buscando por lo que se actualiza el mejor para esta búsqueda
                            best_cost = tour.delta_cost_swap(tour.current, tour.cost, i, j)
                            
                        improved = True
                    else:
                        if self.options.verbose:
                            details = f"{bcolors.OKBLUE} Solución actual: {tour.cost}{bcolors.ENDC}"
                                            
                    # Agregar la informacion a la tabla
                    if details:
                        table.add_row([f"{bcolors.BOLD}{self.evaluations}", 
                                    f"{end-start:.4f}{bcolors.ENDC}", 
                                    f"{details}"
                                    ])
                        details = ''
                        
                    self.evaluations += 1
                    end = timer() # tiempo actual de iteracion
                    
                        
            if improved: # se encontro una mejora en la búsqueda
                tour.swap(a, b)
                self.best_tour.copy(tour)
                best_cost = self.best_tour.cost
                
                details = f"{bcolors.OKGREEN} Solución actual con mejor costo encontrada: {tour.cost}{bcolors.ENDC}"
                table.add_row([f"{bcolors.BOLD}{self.evaluations}", 
                                    f"{end-start:.4f}{bcolors.ENDC}", 
                                    f"{details}"
                                    ])
                details = ''
                # Guardar Trayectoria
                self.trajectory.append( Trajectory(
                                    tour=tour.current.copy(),
                                    cost=tour.cost, 
                                    iterations=self.evaluations, 
                                    evaluations=self.evaluations) )

    
        # actualizar tiempo total de búsqueda 
        self.total_time = timer() - start
            
    """
    
    
    2 - O P T 
    
    
    """

            
    def twoOptSearch(self, tour: Tour, table: PrettyTable = PrettyTable()) -> None:
        """ Aplica la búsqueda por 3-opt """
        #print(tour.current)   
        n = self.problem.getSize()
        if n < 3: 
            return
        
        # tiempo inicial para iteraciones y condicion de termino por tiempo
        start = end = timer()
        a, b = 0, 0
        improved = True
        best_cost = self.best_tour.cost
        
        while improved:
            
            details = '' # variable de texto con los detalles

            improved = False
            
            for i in range(n):
                if improved and not self.bestImprovement: # si es best improvement se continua el loop si no se corta al ser first improvement
                    break
                for j in range(i + 2, n):
                    if improved and not self.bestImprovement:
                        break
                    
                    if tour.delta_cost_two_opt(tour.current, tour.cost, i, j) < best_cost:
                        
                        a, b = i, j # se guardan los indices del optimo local si se encuentra uno mejor
                        
                        if self.bestImprovement: # cuando sea best improvement se sigue buscando por lo que se actualiza el mejor para esta búsqueda
                            best_cost = tour.delta_cost_two_opt(tour.current, tour.cost, i, j)
                            
                        improved = True
                    else:
                        if self.options.verbose:
                            details = f"{bcolors.OKBLUE} Solución actual: {tour.cost}{bcolors.ENDC}"
                                                   
                    # Agregar la informacion a la tabla
                    if details:
                        table.add_row([f"{bcolors.BOLD}{self.evaluations}", 
                                    f"{end-start:.4f}{bcolors.ENDC}", 
                                    f"{details}"
                                    ])
                        details = ''
                        
                    self.evaluations += 1
                    end = timer() # tiempo actual de iteracion
                        
                        
            if improved: # se encontro una mejora en la búsqueda
                tour.twoOptSwap(a, b)
                self.best_tour.copy(tour)
                best_cost = self.best_tour.cost
                
                details = f"{bcolors.OKGREEN} Solución actual con mejor costo encontrada: {tour.cost}{bcolors.ENDC}"
                table.add_row([f"{bcolors.BOLD}{self.evaluations}", 
                                    f"{end-start:.4f}{bcolors.ENDC}", 
                                    f"{details}"
                                    ])
                details = ''
                # Guardar Trayectoria
                self.trajectory.append( Trajectory(
                                    tour=tour.current.copy(),
                                    cost=tour.cost, 
                                    iterations=self.evaluations, 
                                    evaluations=self.evaluations) )
    
        # actualizar tiempo total de búsqueda
        self.total_time = timer() - start
        

    """
    
    
    3 - O P T 
    
    
    """
    
    def threeOptSearch(self, tour: Tour, table: PrettyTable = PrettyTable()) -> None:
        """ Aplica la búsqueda por 3-opt """
        
        n = self.problem.getSize()
        if n < 4:
            return
        
        improved = True
        # tiempo inicial para iteraciones y condicion de termino por tiempo
        start = end = timer()
    
        while improved:
            
            details = '' # variable de texto con los detalles
            
            improved = False
            delta = 0
            for i in range(n):
                if improved and not self.bestImprovement:
                    break
                for j in range(i + 2, n):
                    if improved and not self.bestImprovement:
                        break
                    for k in range(j + 2, n + (i > 0)):
                        if improved and not self.bestImprovement:
                            break
                        
                        delta = tour.bestThreeOptSwap(i, j, k)
                        
                        if delta < 0:
                            
                            self.trajectory.append( Trajectory(
                                    tour=tour.current.copy(),
                                    cost=tour.cost, 
                                    iterations=self.evaluations, 
                                    evaluations=self.evaluations) )
                                
                            self.best_tour.copy(tour)
                                   
                            improved = True
                            details = f"{bcolors.OKGREEN} Solución actual con mejor costo encontrada: {tour.cost}{bcolors.ENDC}"
                        else:
                            if self.options.verbose:     
                                details = f"{bcolors.OKBLUE} Solución actual: {tour.cost}{bcolors.ENDC}"
                            
                            
                        end = timer() # tiempo actual de iteracion
                        if details:
                            # Agregar la informacion a la tabla
                            table.add_row([f"{bcolors.BOLD}{self.evaluations}", 
                                        f"{end-start:.4f}{bcolors.ENDC}", 
                                        f"{details}"
                                        ])
                            details = ''
                            
                        self.evaluations += 1

                                                        
        # actualizar tiempo total de búsqueda
        self.total_time = timer() - start



    def printSolFile(self, outputSol: str) -> None:
        """ Guarda la solución en archivo de texto """
        utilities.printSolToFile(outputSol, self.best_tour.current)

    def printTraFile(self, outputTra: str) -> None:
        """ Guarda la trayectoria de la solución en archivo de texto """
        utilities.printTraToFile(outputTra, self.trajectory)

    def updateLog(self) -> None:
        """ Actualiza el registro de mejores soluciones con todas las caracteristicas de su ejecución """
        # crea la carpeta en caso de que no exista (python 3.5+)
        Path("log/").mkdir(exist_ok=True)
        logFile = "log/LSlog.csv"
        # usar el archivo en modo append
        with open(logFile, "a", newline="\n") as csvfile:
            
            print(f"{bcolors.OKGREEN}\nActualizando log con mejores soluciones en archivo... {bcolors.ENDC}{path.abspath(logFile)}")
            # Headers
            fields = ["solution","cost","instance","date","seed","move","max_evaluations","max_time","initial_solution"]
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
        