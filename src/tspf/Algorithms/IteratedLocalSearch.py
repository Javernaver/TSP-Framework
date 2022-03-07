"""
Modulo que contiene la clase la cual representa el metodo de búsqueda de IteratedLocalSearch

"""

from ..Tools import utilities, bcolors, plot, Trajectory
from . import path, csv, datetime, Path, timer, PrettyTable, LocalSearch
from .. import AlgorithmsOptions, Tsp, Tour, TSPMove, PerturbationType, InitialSolution

class IteratedLocalSearch():
    
    
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
        move_type : TSPMove
            Tipo de movimiento
        perturbation : PerturbationType
            Tipo de perturbacion a aplicar por iteracion
        nPerturbations : int
            Numero de perturbaciones por iteracion
        best_tour : Tour
            Instancia del mejor tour
        evaluations : int
            Numero de evaluaciones
        iterations : int
            Numero de iteraciones
        total_time : float
            Tiempo de ejecucion de Iterated Local Search
        trajectory : list
            Lista de objetos de la trayectoria de la solución
        bestImprovement : bool
            Si es de tipo best improvement o no

        Examples
        --------
        >>> options = AlgorithmsOptions()
        >>> problem = Tsp(filename=options.instance)
        >>> solver = IteratedLocalSearch(options=options, problem=problem)
    """

        # Atributos de instancia
        self.problem: Tsp # Problema TSP
        
        self.move_type: TSPMove # Tipo de movimiento
        
        self.perturbation: PerturbationType # Tipo de Perturbacion
        
        self.nPerturbations = 3 # Numero de perturbaciones
        
        self.best_tour: Tour # Mejor tour
        
        self.iterations = 1 # numero de iteraciones
        
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

        self.move_type = self.options.move
        
        # inicializar mejor tour
        self.best_tour = Tour(problem=self.problem, type_initial_sol=InitialSolution.RANDOM)
        self.perturbation = options.perturbation
        self.nPerturbations = options.nPerturbations
        
        
    def print_best_solution(self) -> None:
        """ Escribir la mejor solución """
        self.updateLog()
        print()
        print(f"\t\t{bcolors.UNDERLINE}Mejor Solución Encontrada{bcolors.ENDC}\n")
        self.best_tour.printSol(True)
        print(f"{bcolors.BOLD}Total de iteraciones:{bcolors.ENDC} {bcolors.OKBLUE}{self.iterations-1}{bcolors.ENDC}")
        print(f"{bcolors.BOLD}Total de evaluaciones:{bcolors.ENDC} {bcolors.OKBLUE}{self.evaluations-1}{bcolors.ENDC}")
        print(f"{bcolors.BOLD}Tiempo total de búsqueda con Iterated Local Search:{bcolors.ENDC} {bcolors.OKBLUE}{self.total_time:.3f} segundos{bcolors.ENDC}")

    
    def search(self, first_solution: Tour = None) -> None:
        """ Ejecuta la búsqueda de Iterated Local Search desde una solución inicial """

        table = PrettyTable()

        table.field_names = [f"{bcolors.BOLD}Iteraciones", "Tiempo", f"Detalles{bcolors.ENDC}"]

        # Si el atributo opcional de la solución inicial no esta incluido
        if not first_solution:
            first_solution = Tour(type_initial_sol=self.options.initial_solution, problem=self.problem)

 
        current_tour = Tour(tour=first_solution) # variable del tour actual 
        
        self.best_tour.copy(first_solution) # solución inicial se guarda como la mejor hasta el momento
        # Guardar trayectoria Final
        self.trajectory.append( Trajectory(
                                tour=self.best_tour.current.copy(),
                                cost=self.best_tour.cost, 
                                iterations=self.iterations-1, 
                                evaluations=self.evaluations-1) )
        if not self.options.replit:
            self.trajectory.append( Trajectory(
                                    tour=self.best_tour.current.copy(),
                                    cost=self.best_tour.cost, 
                                    iterations=self.iterations-1, 
                                    evaluations=self.evaluations-1) )
                                
        print(f"{bcolors.UNDERLINE}\nComenzando búsqueda, solución inicial: {bcolors.ENDC}")
        self.best_tour.printSol()

       
        if not self.options.silent: # si esta o no el modo silencioso que muestra los cambios en cada iteracion
            print(f"{bcolors.HEADER}\nEjecutando Iterated Local Search...\n{bcolors.ENDC}")
            
        
        # tiempo inicial para iteraciones y condicion de termino por tiempo
        start = end = timer()
        
        solver = LocalSearch(options=self.options, problem=self.problem)
        
        
        # Loop principal de ITS   
        while self.terminationCondition(self.iterations, self.evaluations, end-start):
            
            details = ''
            
            # Realizar búsqueda Local Search
            if self.options.move == TSPMove.SWAP:
                solver.swapSearch(current_tour)
            elif self.options.move == TSPMove.TWO_OPT:
                solver.twoOptSearch(current_tour)
            elif self.options.move == TSPMove.THREE_OPT:
                solver.threeOptSearch(current_tour)    
            
            current_tour.copy(solver.best_tour)
            
            # Realizar las Perturbaciones
            for _ in range(self.nPerturbations):
                
                if self.perturbation == PerturbationType.SWAP:
                    current_tour.randomMove(TSPMove.SWAP)
                elif self.perturbation == PerturbationType.TWO_OPT:
                    current_tour.randomMove(TSPMove.TWO_OPT)
                elif self.perturbation == PerturbationType.THREE_OPT:
                    current_tour.randomMove(TSPMove.THREE_OPT)
                elif self.perturbation == PerturbationType.RANDOM:
                    move = utilities.random.choice([m.value for m in TSPMove]) # seleccionar Perturbacion aleatoria
                    current_tour.randomMove(move)

            # si se encontro una mejor solución
            if current_tour.cost < self.best_tour.cost:
                                
                details = f"{bcolors.OKGREEN} Mejor solución encontrada: {current_tour.cost}{bcolors.ENDC}" 
                
                
                self.trajectory.append( Trajectory(
                                tour=current_tour.current.copy(),
                                cost=current_tour.cost, 
                                iterations=self.iterations, 
                                evaluations=solver.evaluations) )
                
                self.best_tour.copy(current_tour)
                
            else:
                details = f"{bcolors.OKBLUE} Solución actual: {current_tour.cost}{bcolors.ENDC}"
               
            
            table.add_row([f"{bcolors.BOLD}{self.iterations}", 
                                    f"{end-start:.4f}{bcolors.ENDC}", 
                                    f"{details}"
                                    ])
            
            #neighbor_tour.copy(current_tour)
            self.iterations += 1
            self.evaluations += 1
            end = timer() # tiempo actual de iteracion


        # actualizar tiempo total de búsqueda 
        self.total_time = timer() - start
        self.evaluations += solver.evaluations
        # Mostrar tabla
        if not self.options.silent:
            print(table)
            #print()
            
        self.trajectory.append( Trajectory(
                                tour=self.best_tour.current.copy(),
                                cost=self.best_tour.cost, 
                                iterations=self.iterations-1,
                                evaluations=solver.evaluations-1) )

    


    def terminationCondition(self, iterations: int, evaluations: int, time: float) -> bool:
        """ Condicion de termino para el ciclo principal de Simulated Annealing, 
        basado en los criterios de evaluaciones y tiempo, devuelve verdadero o falso si se debe continuar o no"""
		
        # Criterio de termino de las  iteraciones
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
        """ Guarda la solución en archivo de texto"""
        utilities.printSolToFile(outputSol, self.best_tour.current)

    def printTraFile(self, outputTra: str) -> None:
        """ Guarda la trayectoria de la solución en archivo de texto"""
        utilities.printTraToFile(outputTra, self.trajectory)

    def updateLog(self) -> None:
        """ Actualiza el registro de mejores soluciones con todas las caracteristicas de su ejecución """
        # crea la carpeta en caso de que no exista (python 3.5+)
        Path("log/").mkdir(exist_ok=True)
        logFile = "log/ILSlog.csv"
        # usar el archivo en modo append
        with open(logFile, "a", newline="\n") as csvfile:
            
            print(f"{bcolors.OKGREEN}\nActualizando log con mejores soluciones en archivo... {bcolors.ENDC}{path.abspath(logFile)}")
            # Headers
            fields = ["solution","cost","instance","date","seed","move","perturbation","nPerturbations","max_evaluations","max_time","initial_solution"]
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
                "perturbation": self.perturbation.value,
                "max_evaluations": self.options.max_evaluations, 
                "max_time": self.options.max_time,
                "initial_solution": self.options.initial_solution.value
            })

    def visualize(self) -> None:
        """ Visualiza la trayectoria de la solución """
        plot.Graph.replit = self.options.replit
        plot.Graph.trajectory = self.trajectory
        
        plot.show(self.options.gui)