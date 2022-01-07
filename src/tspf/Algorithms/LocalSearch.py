"""Modulo que contiene la clase la cual representa el metodo de busqueda de LocalSearch"""

from . import path, csv, datetime, Path, timer, PrettyTable
from .. import AlgorithmsOptions, Tsp, Tour, TSPMove, Trajectory, utilities, plot, InitialSolution, bcolors

class LocalSearch():
    
    
    def __init__(self, options: AlgorithmsOptions = None, problem: Tsp = None) -> None:

        # Atributos de instancia
        self.problem: Tsp # Problema TSP
        
        self.move_type: TSPMove # Tipo de movimiento
        
        self.best_tour: Tour # Mejor tour
        
        self.evaluations = 1 # numero de evaluaciones
        
        self.total_time = 0.0 # tiempo de ejecucion de Simulated Annealing

        self.options: AlgorithmsOptions # Opciones

        self.trajectory = [] # lista con la trayectoria de la solucion
        
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
        self.best_tour = Tour(problem=self.problem, type_initial_sol=InitialSolution.DETERMINISTIC)
        
        
    def print_best_solution(self) -> None:
        """ Escribir la mejor solucion """
        self.updateLog()
        print()
        print(f"\t\t{bcolors.UNDERLINE}Mejor Solucion Encontrada{bcolors.ENDC}\n")
        self.best_tour.printSol(True)
        print(f"{bcolors.BOLD}Total de evaluaciones:{bcolors.ENDC} {bcolors.OKBLUE}{self.evaluations-1}{bcolors.ENDC}")
        print(f"{bcolors.BOLD}Tiempo total de busqueda con Local Search:{bcolors.ENDC} {bcolors.OKBLUE}{self.total_time:.3f} segundos{bcolors.ENDC}")

    
    def search(self, first_solution: Tour = None) -> None:
        """ Ejecuta la busqueda de Local Search desde una solucion inicial """

        table = PrettyTable()

        table.field_names = [f"{bcolors.BOLD}Iteraciones", "Tiempo", f"Detalles{bcolors.ENDC}"]

        # Si el atributo opcional de la solucion inicial no esta incluido
        if not first_solution:
            first_solution = Tour(type_initial_sol=self.options.initial_solution, problem=self.problem)

 
        current_tour = Tour(tour=first_solution) # variable del tour actual
        
        self.best_tour.copy(first_solution) # solucion inicial se guarda como la mejor hasta el momento
        # Guardar trayectoria Final
        self.trajectory.append( Trajectory(
                                tour=self.best_tour.current.copy(),
                                cost=self.best_tour.cost, 
                                iterations=self.evaluations, 
                                evaluations=self.evaluations) )
                                
        print(f"{bcolors.UNDERLINE}\nComenzando busqueda, solucion inicial: {bcolors.ENDC}")
        self.best_tour.printSol()

       
        if not self.options.silent: # si esta o no el modo silencioso que muestra los cambios en cada iteracion
            print(f"{bcolors.HEADER}\nEjecutando Local Search...\n{bcolors.ENDC}")
            #print(f"{bcolors.BOLD}\nIteracion; Temperatura; Tiempo; Detalle{bcolors.ENDC}", end='')
        
        if self.move_type == TSPMove.SWAP:
            pass
        elif self.move_type == TSPMove.TWO_OPT:
            self.twoOPT(current_tour, table)
        elif self.move_type == TSPMove.THREE_OPT:
            self.threeOPT(current_tour, table)
        
        
        # Guardar trayectoria Final
        self.trajectory.append( Trajectory(
                                tour=self.best_tour.current.copy(),
                                cost=self.best_tour.cost, 
                                iterations=self.evaluations-1, 
                                evaluations=self.evaluations-1) ) 

        # Mostrar tabla
        if not self.options.silent:
            print(table)
            #print()
            
            
    def twoOPT(self, tour: Tour, table: PrettyTable, improved: bool = False) -> None:
        """ Aplica la busqueda por 3-opt """
        #print(tour.current)   
        n = self.problem.getSize()
        if n < 2: 
            return
        
        # tiempo inicial para iteraciones y condicion de termino por tiempo
        start = end = timer()
        
        while not improved:
            
            details = '' # variable de texto con los detalles

            improved = False
            
            for i in range(n):
                for j in range(i + 2, n):
                    
                    tour.twoOptSwap(i, j)
                    
                    if tour.cost < self.best_tour.cost:
                        
                        self.trajectory.append( Trajectory(
                            tour=tour.current.copy(),
                            cost=tour.cost, 
                            iterations=self.evaluations-1, 
                            evaluations=self.evaluations-1) )
                        
                        self.best_tour.copy(tour)
                        details = f"{bcolors.OKGREEN} Solucion actual con mejor costo encontrada: {tour.cost}{bcolors.ENDC}"
                        improved = True
                    else:
                        
                        details = f"{bcolors.OKBLUE} Solucion actual: {tour.cost}{bcolors.ENDC}"
                                            
                        
                    # Agregar la informacion a la tabla
                    table.add_row([f"{bcolors.BOLD}{self.evaluations}", 
                                f"{end-start:.4f}{bcolors.ENDC}", 
                                f"{details}"
                                ])
                    self.evaluations += 1
                    end = timer() # tiempo actual de iteracion
                    if not self.terminationCondition(self.evaluations, end-start):
                        self.total_time = timer() - start
                        return
                        
            
        # actualizar tiempo total de busqueda de Simulated Annealing
        self.total_time = timer() - start


    """ 3 - O P T """
    
    def threeOPT(self, tour: Tour, table: PrettyTable, improved: bool = False) -> None:
        """ Aplica la busqueda por 3-opt """
        #print(tour.current)   
        n = self.problem.getSize()
        if n < 2: 
            return
        
        # tiempo inicial para iteraciones y condicion de termino por tiempo
        start = end = timer()
        
        while not improved:
            
            details = '' # variable de texto con los detalles

            improved = False
            delta = 0
            
            for i in range(n):
                for j in range(i + 2, n):
                    for k in range(j + 2, n + (i > 0)):
                        
                        delta += tour.bestThreeOptSwap(i, j, k)
                        
                        if tour.cost < self.best_tour.cost:
                            
                            self.trajectory.append( Trajectory(
                                tour=tour.current.copy(),
                                cost=tour.cost, 
                                iterations=self.evaluations-1, 
                                evaluations=self.evaluations-1) )
                            
                            self.best_tour.copy(tour)
                            details = f"{bcolors.OKGREEN} Solucion actual con mejor costo encontrada: {tour.cost}{bcolors.ENDC}"

                        else:
                            
                            details = f"{bcolors.OKBLUE} Solucion actual: {tour.cost}{bcolors.ENDC}"
                            
                            
                        
                        if delta >= 0:
                            improved = True
                            
                        # Agregar la informacion a la tabla
                        table.add_row([f"{bcolors.BOLD}{self.evaluations}", 
                                    f"{end-start:.4f}{bcolors.ENDC}", 
                                    f"{details}"
                                    ])
                        self.evaluations += 1
                        end = timer() # tiempo actual de iteracion
                        if not self.terminationCondition(self.evaluations, end-start):
                            self.total_time = timer() - start
                            return
                        
            
        # actualizar tiempo total de busqueda de Simulated Annealing
        self.total_time = timer() - start



    def terminationCondition(self, evaluations: int, time: float) -> bool:
        """ Condicion de termino para el ciclo principal de Simulated Annealing, 
        basado en los criterios de evaluaciones y tiempo, devuelve verdadero o falso si se debe continuar o no"""
		
        # Criterio de termino de las evaluciones | iteraciones
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

            # crear texto con la solucion separando cada elemento con espacios y luego guardarlo en el archivo
            sol = " ".join([str(elem) for elem in self.best_tour.current])

            # escribir la mejor solucion y todas las caracteristicas de su ejecucion
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

    def visualize(self, replit: bool) -> None:
        """ Visualiza la trayectoria de la solucion"""
        plot.replit = replit
        plot.trajectory = self.trajectory
        plot.show()
        