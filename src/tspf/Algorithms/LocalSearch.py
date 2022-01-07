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
        print(f"{bcolors.BOLD}Tiempo total de busqueda con Simulated Annealing:{bcolors.ENDC} {bcolors.OKBLUE}{self.total_time:.3f} segundos{bcolors.ENDC}")

    
    def search(self, first_solution: Tour = None) -> None:
        """ Ejecuta la busqueda de Local Search desde una solucion inicial """

        table = PrettyTable()

        table.field_names = [f"{bcolors.BOLD}Iteraciones", "Tiempo", f"Detalles{bcolors.ENDC}"]

        # Si el atributo opcional de la solucion inicial no esta incluido
        if not first_solution:
            first_solution = Tour(type_initial_sol=self.options.initial_solution, problem=self.problem)

 
        current_tour = Tour(tour=first_solution) # variable del tour actual 
        neighbor_tour = Tour(tour=first_solution) # variable del tour vecino generado 
        
        self.best_tour.copy(first_solution) # solucion inicial se guarda como la mejor hasta el momento
        # Guardar trayectoria Final
        self.trajectory.append( Trajectory(
                                tour=self.best_tour.current.copy(),
                                cost=self.best_tour.cost, 
                                iterations=self.evaluations-1, 
                                evaluations=self.evaluations-1) )
                                
        print(f"{bcolors.UNDERLINE}\nComenzando busqueda, solucion inicial: {bcolors.ENDC}")
        self.best_tour.printSol()

        # tiempo inicial para iteraciones y condicion de termino por tiempo
        start = end = timer()
        if not self.options.silent: # si esta o no el modo silencioso que muestra los cambios en cada iteracion
            print(f"{bcolors.HEADER}\nEjecutando Local Search...\n{bcolors.ENDC}")
            #print(f"{bcolors.BOLD}\nIteracion; Temperatura; Tiempo; Detalle{bcolors.ENDC}", end='')

        # Bucle principal del algoritmo
        while (self.terminationCondition(self.evaluations, end-start)):

            details = '' # variable de texto con los detalles
            self.threeOPT(current_tour)
            #self.best_tour.current.pop()
            #self.three_opt(self.best_tour.current)
            #self.best_tour.current.append(self.best_tour.current[0])
            """ # Generar un vecino aleatoriamente a traves de un movimiento
            neighbor_tour.randomMove(self.move_type)

            # Mostrar avance iteracion
            #if not self.options.silent:
            #    print(f"{bcolors.BOLD}\n{self.evaluations}; {temperature:.2f}; {end-start:.4f}; {bcolors.ENDC}", end='')

            # Revisar funcion objetivo de la nueva solucion
            if (neighbor_tour.cost < current_tour.cost):
                # Mejor solucion encontrada
                current_tour.copy(neighbor_tour)
                # Guardar trayectoria Final
                self.trajectory.append( Trajectory(
                                        tour=current_tour.current.copy(),
                                        cost=current_tour.cost, 
                                        iterations=self.evaluations, 
                                        evaluations=self.evaluations,
                                        temperature=temperature) ) 

                #if not self.options.silent:
                #    print(f"{bcolors.OKGREEN} Solucion actual con mejor costo encontrada: {current_tour.cost}{bcolors.ENDC}", end='')

                details += f"{bcolors.OKGREEN} Solucion actual con mejor costo encontrada: {current_tour.cost}{bcolors.ENDC}"

            else:
                # Calcular criterio de aceptacion
                prob = self.getAcceptanceProbability(neighbor_tour.cost, current_tour.cost, temperature)
                
                if (utilities.random.random() <= prob):
                    # Se acepta la solucion peor
                    current_tour.copy(neighbor_tour)
                    
                    #if not self.options.silent:
                    #    print(f"{bcolors.FAIL} Se acepta peor costo por criterio de metropolis: {neighbor_tour.cost}{bcolors.ENDC}", end='')
                    
                    details += f"{bcolors.FAIL} Se acepta peor costo por criterio de metropolis: {neighbor_tour.cost}{bcolors.ENDC}"
                else:
                    #if not self.options.silent:
                    #    print(f"{bcolors.WARNING} No se acepta peor costo por criterio de metropolis: {neighbor_tour.cost}{bcolors.ENDC}{bcolors.OKGREEN} -> Solucion actual: {current_tour.cost}{bcolors.ENDC}", end='')
                    # No se acepta la solucion
                    details += f"{bcolors.WARNING} No se acepta peor costo por criterio de metropolis: {neighbor_tour.cost}{bcolors.ENDC}{bcolors.OKGREEN} -> Solucion actual: {current_tour.cost}{bcolors.ENDC}"

                    neighbor_tour.copy(current_tour)

			# Revisar si la nueva solucion es la mejor hasta el momento
            if (current_tour.cost < self.best_tour.cost):
                #if not self.options.silent:
                #    print(f"{bcolors.OKGREEN} -> ¡Mejor solucion global encontrada! {bcolors.ENDC}", end='')
                
                details += f"{bcolors.OKGREEN} -> ¡Mejor solucion global encontrada! {bcolors.ENDC}"

                self.best_tour.copy(current_tour) """

            # Agregar la informacion a la tabla
            table.add_row([f"{bcolors.BOLD}{self.evaluations}", 
                        f"{end-start:.4f}{bcolors.ENDC}", 
                        f"{details}"
                        ])
                    
            self.evaluations += 1
            end = timer() # tiempo actual de iteracion

        # actualizar tiempo total de busqueda de Simulated Annealing
        self.total_time = timer() - start
        # Guardar trayectoria Final
        

        # Mostrar tabla
        if not self.options.silent:
            print(table)
            #print()


    def terminationCondition(self, evaluations: int, time: float) -> bool:
        """ Condicion de termino para el ciclo principal de Simulated Annealing, 
        basado en los criterios de evaluaciones y tiempo, devuelve verdadero o falso si se debe continuar o no"""
		
        # Criterio de termino de las evaluciones | iteraciones
        if (self.options.max_evaluations > 0 or self.options.max_iterations):
            if (evaluations > self.options.max_evaluations or evaluations > self.options.max_iterations):
                return False
        
        # Criterio de termino por tiempo
        if (self.options.max_time > 0):
            if (time > self.options.max_time):
                return False
        
        return True
        
        
        
    """ 3 - O P T """
    def threeOPT(self, tour: Tour, improved: bool = False) -> None:
        """ Aplica la busqueda por 3-opt """
        #print(tour.current)   
        n = self.problem.getSize()
        if n < 2: 
            return
        
        tour.current.pop()
        
        while not improved:
            improved = False
            delta = 0
            for i in range(n):
                for j in range(i + 2, n):
                    for k in range(j + 2, n + (i > 0)):
                        delta += tour.bestThreeOptSwap(i, j, k)
                        
                        if tour.cost < self.best_tour.cost:
                            tour.current.append(tour.current[0])
                            self.trajectory.append( Trajectory(
                                tour=tour.current.copy(),
                                cost=tour.cost, 
                                iterations=self.evaluations-1, 
                                evaluations=self.evaluations-1) )
                            self.best_tour.copy(tour)
                            tour.current.pop()
                            
                        if delta >= 0:
                            improved = True
        
        tour.current.append(tour.current[0])
        


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
        