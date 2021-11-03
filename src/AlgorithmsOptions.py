"""Modulo que contiene las clases encargadas de todas las opciones que puedan tener los demas modulos"""

from . import Enum, time, argparse, bcolors, utilities

class MHType(Enum):
    """Tipos de Metaheristicas disponibles
    SA: Simulated Annealing
    GA: Genetic Algorithm
    """
    SA = 'SA'
    GA = 'GA'

class TSPMove(Enum):
    """Tipos de movimientos disponibles para el TSP 
    TWO_OPT: Operador 2-opt
    SWAP: Operador swap
    """
    TWO_OPT = 'TWO_OPT'
    SWAP = 'SWAP'

""" Simulated Annealing """

class InitialSolution(Enum):
    """ Metodos disponibles para crear una solucion inicial
    RANDOM: Solucion aleatoria
    NEAREST_N: Solucion creada con la heuristica del vecino mas cercano
    DETERMINISTIC: Solucion creada deterministicamente para testing, en este caso es secuencial
    """
    RANDOM = 'RANDOM'
    NEAREST_N = 'NEAREST_N'
    DETERMINISTIC = 'DETERMINISTIC'

class CoolingType(Enum):
    """Esquemas de enfriamiento disponibles para Simulated Annealing
    GEOMETRIC: t = t * alpha
    LINEAR: t = t * (1 - (evaluation / max_evaluations))
    LOG: t = (t * alpha) * 1 / (ln(evaluation) + 1)
    """
    GEOMETRIC = 'GEOMETRIC'
    LINEAR = 'LINEAR'
    LOG = 'LOG'

""" Algoritmo Genetico """

class SelectionType(Enum):
    """Tipos de seleccion de individuos
        RANDOM: Seleccion aleatoria
        BEST: Seleccion de los mejores (elitismo)
        ROULETTE: Seleccion proporcional al fitness
        TOURNAMENT: Seleccion de torneos k=3
    """
    RANDOM = 'RANDOM'
    BEST = 'BEST'
    ROULETTE = 'ROULETTE'
    TOURNAMENT = 'TOURNAMENT'

class CrossoverType(Enum):
    """Tipos de cruzamiento disponibles
        PMX: (partially-mapped crossover) hace swap adaptando los tours
        O1X: (order 1 crossover) 
        OPX: (one point crossover) se realiza cruzamiento en un punto utilizando una lista de referencia 
    """
    PMX = 'PMX'
    OX = 'OX'
    OPX = 'OPX'

class SelectionStrategy(Enum):
    """Estrategias de seleccion de individuos de la poblacion
    MU_LAMBDA: Estrategia (mu, lambda)
    MUPLUSLAMBDA: Estrategia (mu+lambda)
    """
    MULAMBDA = 'MULAMBDA'
    MUPLUSLAMBDA = 'MUPLUSLAMBDA'

class AlgorithmsOptions():
    """
    Clase para configurar y leer todas las opciones que pueda tener una metaheristica recibidas como atributo o como definiciones

    Attributes
    ----------
    output : str
        Archivo para imprimir la solucion
    instance : str
        Archivo de la instancia TSP con formato TSPLib
    seed : int
        Semilla para el generador de numero aleatorios
    metaheuristic : Enum
        Tipo de metaheuristica a ejecutar SA o GA
    move : Enum
        Tipo del movimiento para la metaheuristica
    max_evaluations : int
        Evaluaciones maximas 
    alpha : float
        Parametro alfa para el enfriamiento de SA
    t0 : float
        Temperatura inicial para SA
    tmin : float
        Temperatura minima para SA
    cooling : Enum
        Tipo de enfriamiento para SA
    pop_size : int
        Tamaño de la poblacion 
    offspring_size : int
        Cantidad de hijos      
    pselection_type : Enum
        Seleccion de padres       
    crossover_type : Enum
        Cruzamiento
    mutation_type : Enum
        Mutacion
    mutation_prob : float
        Probabilidad de mutacion
    selection_strategy : Enum
        Estrategia de seleccion de la nueva poblacion
    gselection_type : Enum
        Seleccion de la nueva poblacion
    Methods
    -------
    __init__(args: list, **kwargs: dict)
        Constructor de clase para configurar y leer todas las opciones que pueda tener una metaheristica recibidas como atributo
    readOptions(argv :list, kwargs: dict)
        Clase que lee las opciones introducidas como atributo y por definicion
    validateOptions()
        Validar que algunos paramaetros para los algoritmos sean coerentes
    generalArgs(args :any, kwargs: dict)
        Procesar los argumentos generales, se pregunta se llego por argumento o por definicion, luego se asigna segun venga dando prioridad a los argumentos
    saArgs(args :any, kwargs: dict)
        Procesar los argumentos de Simulated Annealing
    gaArgs(args :any, kwargs: dict)
        Procesar los argumentos de Algoritmo Genetico
    printOptions()
        Mostrar las opciones y parametros finales
    """
    
    # OPCIONES GENERALES
    
    output = "solution.txt"	# Archivo para imprimir la solucion

    trajectory = "trajectory.csv"	# Archivo para imprimir la trayectoria de solucion
    
    instance = "instances/burma14.tsp" # Archivo de la instancia    
    
    seed = 0 # Semilla para el generador de numero aleatorios    
     
    metaheuristic = MHType.SA # Tipo de metaheuristica a ejecutar   
     
    move = TSPMove.SWAP # Tipo del movimiento para la metaheuristica
    
    max_evaluations = 1000 # Evaluaciones maximas
    
    max_iterations = 20 # Numero de iteraciones maximas
    
    max_time = 60.0 # Tiempo de ejecucion maximo
    
    initial_solution = InitialSolution.DETERMINISTIC # Solucion Inicial
    
    silent = False # Modo silencioso

    visualize = False # Visualizacion de la trayectoria

    replit = False # Si se esta ejecutando en Replit.com ya que causa inconveniencia con la graficacion

    # OPCIONES PARA SIMULATED ANNEALING 
    
    alpha = 0.98 # Parametro alfa para el enfriamiento
    
    t0 = 1000.0 # Temperatura inicial 
    
    tmin = 900.0 # Temperatura minima    
    
    cooling = CoolingType.GEOMETRIC # Tipo de enfriamiento

    # OPCIONES PARA ALGORITMO GENETICO 
    
    pop_size = 10 # Tamaño de la poblacion 
	
    offspring_size = 20 # Cantidad de hijos
    
    pselection_type = SelectionType.RANDOM # Seleccion de padres
    
    crossover_type = CrossoverType.OX # Cruzamiento
    
    mutation_type = TSPMove.SWAP # Mutacion
    
    mutation_prob = 0.2 # probabilidad de mutacion 
    
    selection_strategy = SelectionStrategy.MULAMBDA # Estrategia de seleccion de la nueva poblacion
    
    gselection_type = SelectionType.RANDOM # Seleccion de la nueva poblacion

    def __init__(self, argv=[], **kwargs) -> None:

        # Semilla para el generador de numeros aleatorios
        self.seed = round(time.time() * 1000)
        
        # Leer argumentos que vengan por parametro o por definicion
        self.readOptions(argv, kwargs)

        # definir semilla para el generador aleatorio
        utilities.random.seed(self.seed)
        # Mostrar Opciones 
        self.printOptions()
    

    def readOptions(self, argv: list, kwargs: dict) -> None:
        """ Leer las opciones introducidas como atributo y como definicion """
        # Si no se introdujeron argumentos
        if (len(argv) == 1 or not argv):
            print(f"{bcolors.WARNING}Warning: usando instancia por defecto: {self.instance} {bcolors.ENDC}")
            print(f"{bcolors.WARNING}Si desea utilizar otra instancia debe proporcionarla (use -i o --instance <file_path>) {bcolors.ENDC}")
            print(f"{bcolors.WARNING}Use el argumento '-h' o '--help' para mayor informacion {bcolors.ENDC}")
        
        parser = argparse.ArgumentParser()
        # Declarar y definir argumentos
        # Definir argumentos generales
        parser.add_argument("-s", "--silent", help="Ejecuta sin mostrar los cambios en cada ciclo de los algoritmos", action="store_true")
        parser.add_argument("-vi", "--visualize", help="Muestra la visualizacion de trayectoria a la mejor solucion de forma grafica", action="store_true")
        parser.add_argument("-re", "--replit", help="Si se ejecuta en Replit.com ya que la visualizacion puede tener inconvenientes", action="store_true")

        parser.add_argument("-mh", "--metaheuristic", help="Tipo de Metaherisitica a usar:\n SA: Simulated Annealing\n GA: Genetic Algorithm")
        parser.add_argument("-i", "--instance", help="Archivo con la instancia a utilizar en formato TSPLIB")
        parser.add_argument("-se", "--seed", help="Numero para ser usado como semilla para el generador de numeros aleatorios")
        parser.add_argument("-out", "--output", help="Nombre del archivo de salida para la solucion")
        parser.add_argument("-tra", "--trajectory", help="Nombre del archivo de salida para la trayectoria de la solucion")
        parser.add_argument("-mhm", "--move", help="Tipo de movimiento a utilizar en la heuristica [ 2opt | swap ]")
        parser.add_argument("-e", "--evaluations", help="Numero maximo de soluciones a evaluar")
        parser.add_argument("-it", "--iterations", help="Numero maximo de iteraciones a realizar")
        parser.add_argument("-t", "--time", help="Limite de tiempo de ejecucion en segundos")

        # Definir argumentos de Simulated Annealing
        parser.add_argument("-is", "--insol", help="Solucion inicial [ RANDOM | NEAREST_N | DETERMINISTIC ]")
        parser.add_argument("-a", "--alpha", help="Parametro alfa para el esquema geometrico ]0,1]")
        parser.add_argument("-t0", "--tini", help="Temperatura inicial ]0,DOUBLE_MAX]")
        parser.add_argument("-tm", "--tmin", help="Temperatura minima ]0,DOUBLE_MAX]")
        parser.add_argument("-c", "--cooling", help="Esquema de enfriamiento de la temperatura [ geometric | log | linear ]")

        # Definir argumentos de Algoritmo Genetico
        parser.add_argument("-p", "--psize", help="Tamaño de la poblacion ]0,INT_MAX]")
        parser.add_argument("-o", "--osize", help="Cantidad de hijos a generar ]0,INT_MAX]")
        parser.add_argument("-ps", "--pselection", help="Operador de seleccion de padres [ random | best | roulette | tournament ]")
        parser.add_argument("-cr", "--crossover", help="Operador de crossover [ ox | opx | pmx ]")
        parser.add_argument("-mu", "--mutation", help="Operador de mutacion [ swap | 2opt ]")
        parser.add_argument("-mp", "--mprobability", help="Probabilidad de mutacion [0.0,1.0]")
        parser.add_argument("-gs", "--gselection", help="Operador de seleccion de poblacion [ random | best | roulette | tournament ]")
        parser.add_argument("-g", "--gstrategy", help="Estrategia de seleccion de padres [ mu,lambda | mu+lambda ]")
        # Procesar argumentos
        args = parser.parse_args()

        # Procesar argumentos generales
        self.argsGeneral(args, kwargs)
        
        if self.metaheuristic == MHType.SA:
            # Procesar argumentos de Simulated Annealing
            self.argsSA(args, kwargs)
            # Validar logica de opciones
            self.validOptSA()
        elif self.metaheuristic == MHType.GA:
            # Procesar argumentos de Algoritmo Genetico
            self.argsGA(args, kwargs) 
            # Validar logica de opciones
            self.validOptGA() 
        

    def argsGeneral(self, args: argparse.Namespace, kwargs: dict) -> None:
        """Procesar los argumentos generales, se pregunta se llego por argumento o por definicion, luego se asigna segun venga dando prioridad a los argumentos"""
        # Maximo tiempo de ejecucion 
        if (args.time or 'time' in kwargs):
            try:
                self.max_time = float(args.time) if args.time else float(kwargs['time'])
            except: 
                print(f"{bcolors.FAIL}Error: El tiempo maximo debe ser un numero (-t o --time){bcolors.ENDC}")

        # Semilla 
        if (args.seed or 'seed' in kwargs):
            try:
                self.seed = int(args.seed) if args.seed else int(kwargs['seed'])
            except: 
                print(f"{bcolors.FAIL}Error: La semilla debe ser un numero entero (-s o --seed){bcolors.ENDC}")

        # Archivo de salida para solucion
        if (args.output or 'output' in kwargs):
            self.output = args.output if args.output else kwargs['output']

        # Archivo de salida para trayectoria
        if (args.trajectory or 'trajectory' in kwargs):
            self.trajectory = args.trajectory if args.trajectory else kwargs['trajectory']

        # Si se visualizara la trayectoria
        if (args.visualize or 'graphic' in kwargs):
            self.visualize = args.visualize if args.visualize else kwargs['visualize']

        # Si se ejecuta en Replit.com
        if (args.replit or 'replit' in kwargs):
            self.replit = args.replit if args.replit else kwargs['replit']

        # Archivo de instancia
        if (args.instance or 'instance' in kwargs):
            self.instance = args.instance if args.instance else kwargs['instance']

        # Seleccion de Metaheuristica
        if (args.metaheuristic or 'metaheuristic' in kwargs):
            val = args.metaheuristic.upper() if args.metaheuristic else kwargs['metaheuristic'].upper()
            if (val == 'SA'):
                self.metaheuristic = MHType.SA
            elif (val == 'GA'):
                self.metaheuristic = MHType.GA
            else: print(f"{bcolors.FAIL}Error: Metaheuristica no reconocida (-mh o --metaheristic) {bcolors.ENDC}")  
        
        # Numero maximo de evaluaciones
        if (args.evaluations or 'evaluations' in kwargs):
            try:
                self.max_evaluations = int(args.evaluations) if args.evaluations else int(kwargs['evaluations'])
            except: 
                print(f"{bcolors.FAIL}Error: El numero de evaluaciones debe ser un numero entero (-e o --evaluations) {bcolors.ENDC}")

        # Numero maximo de iteraciones
        if (args.iterations or 'iterations' in kwargs):
            try:
                self.max_iterations = int(args.iterations) if args.iterations else int(kwargs['iterations'])
            except: 
                print(f"{bcolors.FAIL}Error: El numero de iteraciones debe ser un numero entero (-it o --iterations) {bcolors.ENDC}")

        # Seleccion del movimiento para la metaheuristica
        if (args.move or 'move' in kwargs):
            val = args.move.lower() if args.move else kwargs['move'].lower()
            if (val == '2opt' or val == '2-opt'):
                self.move = TSPMove.TWO_OPT
            elif (val == 'swap'):
                self.move = TSPMove.SWAP
            else: print(f"{bcolors.FAIL}Error: Tipo de movimiento no reconocido (-mhm o --move) {bcolors.ENDC}") 

        # Modo de salida reducido para no mostrar todos los cambios en los ciclos de los algoritmos
        if (args.silent):
            self.silent = True


    def argsSA(self, args: argparse.Namespace, kwargs: dict) -> None:
        """Procesar los argumentos de Simulated Annealing"""
        # Solucion inicial
        if (args.insol or 'insol' in kwargs):
            val = args.insol.upper() if args.insol else kwargs['insol'].upper()
            if (val == 'RANDOM'):
                self.initial_solution = InitialSolution.RANDOM
            elif (val == 'NEAREST_N'):
                self.initial_solution = InitialSolution.NEAREST_N
            elif (val == 'DETERMINISTIC'):
                self.initial_solution = InitialSolution.DETERMINISTIC
            else: print(f"{bcolors.FAIL}Error: Opcion no reconocida en solucion inicial (-is o --inso) {bcolors.ENDC}")

        # Seleccion del esquema de enfriamiento
        if (args.cooling or 'cooling' in kwargs):
            val = args.cooling.lower() if args.cooling else kwargs['cooling'].lower()
            if (val == 'geometric'):
                self.cooling = CoolingType.GEOMETRIC
            elif (val == 'log'):
                self.cooling = CoolingType.LOG
            elif (val == 'linear'):
                self.cooling = CoolingType.LINEAR    
            else: print(f"{bcolors.FAIL}Error: Opcion no reconocida en COOLING (-tc o --cooling) {bcolors.ENDC}")    

        # Parametro alpha
        if (args.alpha or 'alpha' in kwargs):
            try:
                self.alpha = float(args.alpha) if args.alpha else float(kwargs['alpha'])
            except: 
                print(f"{bcolors.FAIL}Error: El valor de alpha debe ser un numero en (-a o --alpha) {bcolors.ENDC}")
        
        # Temperatura inicial
        if (args.tini or 'tini' in kwargs):
            try:
                self.t0 = float(args.tini) if args.tini else float(kwargs['tini'])
            except:
                print(f"{bcolors.FAIL}Error: El valor de la temperatura inicial debe ser un numero (-t0 o --tini) {bcolors.ENDC}")

        # Temperatura minima
        if (args.tmin or 'tmin' in kwargs):
            try:
                self.tmin = float(args.tmin) if args.tmin else float(kwargs['tmin'])
            except:
                print(f"{bcolors.FAIL}Error: El valor de la temperatura minima debe ser un numero (-tmin o --tmin) {bcolors.ENDC}")


    def argsGA(self, args: argparse.Namespace, kwargs: dict) -> None:
        """Procesar los argumentos de Algoritmo Genetico"""
        # Tamaño de la poblacion
        if (args.psize or 'psize' in kwargs):
            try:
                self.pop_size = int(args.psize) if args.psize else int(kwargs['psize'])
            except: 
                print(f"{bcolors.FAIL}Error: El tamaño de la poblacion debe ser un numero entero (-p o --psize){bcolors.ENDC}")

        # Cantidad de hijos a generar
        if (args.osize or 'osize' in kwargs):
            try:
                self.offspring_size = int(args.osize) if args.osize else int(kwargs['osize'])
            except: 
                print(f"{bcolors.FAIL}Error: La cantidad de hijos debe ser un numero entero (-o o --osize){bcolors.ENDC}")

        # Seleccion de padres
        if (args.pselection or 'pselection' in kwargs):
            val = args.pselection.lower() if args.pselection else kwargs['pselection'].lower()
            if (val == 'random'):
                self.pselection_type = SelectionType.RANDOM
            elif (val == 'best'):
                self.pselection_type = SelectionType.BEST
            elif (val == 'roulette'):
                self.pselection_type = SelectionType.ROULETTE
            elif (val == 'tournament'):
                self.pselection_type = SelectionType.TOURNAMENT   
            else: print(f"{bcolors.FAIL}Error: Opcion no reconocida en Seleccion de padres (-ps o --pselection) {bcolors.ENDC}")
        
        # Operador de Cruzamiento
        if (args.crossover or 'crossover' in kwargs):
            val = args.crossover.lower() if args.crossover else kwargs['crossover'].lower()
            if (val == 'ox'):
                self.crossover_type = CrossoverType.OX
            elif (val == 'opx'):
                self.crossover_type = CrossoverType.OPX
            elif (val == 'pmx'):
                self.crossover_type = CrossoverType.PMX
            else: print(f"{bcolors.FAIL}Error: Opcion no reconocida en Operador de Cruzamiento (-o o --crossover) {bcolors.ENDC}")

        # Operador de mutacion
        if (args.mutation or 'mutation' in kwargs):
            val = args.mutation.lower() if args.mutation else kwargs['mutation'].lower()
            if (val == '2opt' or val == '2-opt'):
                self.mutation_type = TSPMove.TWO_OPT
            elif (val == 'swap'):
                self.mutation_type = TSPMove.SWAP
            else: print(f"{bcolors.FAIL}Error: Tipo de mutacion no reconocido (-mu o --mutation) {bcolors.ENDC}")

        # Probabilidad de mutacion
        if (args.mprobability or 'mprobability' in kwargs):
            try:
                self.mutation_prob = float(args.mprobability) if args.mprobability else float(kwargs['mprobability'])
            except: 
                print(f"{bcolors.FAIL}Error: El valor de probabilidad de mutacion debe ser un numero en (-mp o --mprobability) {bcolors.ENDC}")
        
        # Operador de seleccion de poblacion
        if (args.gselection or 'gselection' in kwargs):
            val = args.gselection.lower() if args.gselection else kwargs['gselection'].lower()
            if (val == 'random'):
                self.gselection_type = SelectionType.RANDOM
            elif (val == 'best'):
                self.gselection_type = SelectionType.BEST
            elif (val == 'roulette'):
                self.gselection_type = SelectionType.ROULETTE
            elif (val == 'tournament'):
                self.gselection_type = SelectionType.TOURNAMENT   
            else: print(f"{bcolors.FAIL}Error: Opcion no reconocida en Seleccion de poblacion (-gs o --gselection) {bcolors.ENDC}")

        # Estrategia de seleccion de padres
        if (args.gstrategy or 'gstrategy' in kwargs):
            val = args.gstrategy.lower() if args.gstrategy else kwargs['gstrategy'].lower()
            if (val == 'mu,lambda'):
                self.selection_strategy = SelectionStrategy.MULAMBDA
            elif (val == 'mu+lambda'):
                self.selection_strategy = SelectionStrategy.MUPLUSLAMBDA
            else: print(f"{bcolors.FAIL}Error: Tipo de seleccion de padres no reconocido (-g o --gstrategy) {bcolors.ENDC}")


    def validOptSA(self) -> None:
        """ Validar que algunos parametros cumplan con la logica del algoritmo a aplicar """
        if (self.max_evaluations <= 0 or self.max_iterations <= 0):
            print(f"{bcolors.FAIL}Error: iteraciones o evaluaciones maximas deben ser > 0 Iteraciones: {self.max_iterations} Evaluaciones: {self.max_evaluations}{bcolors.ENDC}")
            exit()
        if (self.tmin <= 0 or self.t0 <= 0):
            print(f"{bcolors.FAIL}Error: Las temperatura minima y la temperatura inicial maximas deben ser > 0, tmin: {self.tmin} t0: {self.t0} evaluaciones: {self.max_evaluations} {bcolors.ENDC}")
            exit()
        if (self.alpha <= 0 or self.alpha > 1):
            print(f"{bcolors.FAIL}Error: alfa debe ser > 0 y <= 1, valor: {self.alpha} {bcolors.ENDC}")
            exit()
        if (self.t0 <= self.tmin):
            print(f"{bcolors.FAIL}Error: t0 debe ser > tmin, valor tmin: {self.tmin} valor t0: {self.t0}{bcolors.ENDC}")
            exit()
    
    def validOptGA(self) -> None:
        """ Validar que algunos parametros cumplan con la logica del algoritmo a aplicar """
        if (self.max_evaluations <= 0 or self.max_iterations <= 0):
            print(f"{bcolors.FAIL}Error: iteraciones o evaluaciones maximas deben ser > 0 Iteraciones: {self.max_iterations} Evaluaciones: {self.max_evaluations}{bcolors.ENDC}")
            exit()
        if (self.mutation_prob > 1.0 or self.mutation_prob < 0.0 ):
            print(f"{bcolors.FAIL}Error: la probabilidad de mutacion debe ser [0.0, 1.0]: {self.mutation_prob}{bcolors.ENDC}")
            exit()
        if (self.selection_strategy == SelectionStrategy.MULAMBDA and self.pop_size > self.offspring_size):
            print(f"{bcolors.FAIL}Error: con (mu,lambda) la poblacion (-p/psize) debe ser >= que los hijos (-o/osize){bcolors.ENDC}")
            exit()
        if (self.pop_size <= 1):
            print(f"{bcolors.FAIL}Error: tamaño de la poblacion (-p/psize) debe ser > 1{bcolors.ENDC}")
            exit()
                   
    def printOptions(self) -> None:
        """ Mostrar las opciones y parametros finales """
        # Opciones generales
        print(f"{bcolors.HEADER}\n\t\tOPCIONES GENERALES\n {bcolors.ENDC}")        
        print(f"{bcolors.OKBLUE}Archivo de instancia: {bcolors.ENDC}{self.instance}")
        print(f"{bcolors.OKBLUE}Archivo para imprimir la solucion: {bcolors.ENDC}{self.output}")
        print(f"{bcolors.OKBLUE}Tipo de metaheuristica a ejecutar: {bcolors.ENDC}{self.metaheuristic.value}")
        print(f"{bcolors.OKBLUE}Tipo del movimiento para la metaheuristica: {bcolors.ENDC}{self.move.value}")
        print(f"{bcolors.OKBLUE}Semilla para el generador de numero aleatorios: {bcolors.ENDC}{self.seed}")
        print(f"{bcolors.OKBLUE}Evaluaciones maximas: {bcolors.ENDC}{self.max_evaluations}")
        print(f"{bcolors.OKBLUE}Iteraciones maximas: {bcolors.ENDC}{self.max_iterations}")
        print(f"{bcolors.OKBLUE}Solucion Inicial: {bcolors.ENDC}{self.initial_solution.value}")
        print(f"{bcolors.OKBLUE}Limite de tiempo de ejecucion: {bcolors.ENDC}{self.max_time} segundos")

        # Opciones para Simulated Annealing
        if (self.metaheuristic == MHType.SA):
            print(f"{bcolors.HEADER}\n\t\tOPCIONES PARA SIMULATED ANNEALING\n {bcolors.ENDC}")        
            print(f"{bcolors.OKBLUE}Parametro alfa para el enfriamiento: {bcolors.ENDC}{self.alpha}")
            print(f"{bcolors.OKBLUE}Temperatura inicial: {bcolors.ENDC}{self.t0}")
            print(f"{bcolors.OKBLUE}Temperatura minima: {bcolors.ENDC}{self.tmin}")
            print(f"{bcolors.OKBLUE}Tipo de enfriamiento: {bcolors.ENDC}{self.cooling.value}")
        elif (self.metaheuristic == MHType.GA): # Opciones para Algoritmo Genetico
            print(f"{bcolors.HEADER}\n\t\tOPCIONES PARA ALGORITMO GENETICO\n {bcolors.ENDC}")        
            print(f"{bcolors.OKBLUE}Tamaño de la poblacion: {bcolors.ENDC}{self.pop_size}")
            print(f"{bcolors.OKBLUE}Cantidad de hijos: {bcolors.ENDC}{self.offspring_size}")
            print(f"{bcolors.OKBLUE}Seleccion de padres: {bcolors.ENDC}{self.pselection_type.value}")
            print(f"{bcolors.OKBLUE}Tipo de cruzamiento: {bcolors.ENDC}{self.crossover_type.value}")
            print(f"{bcolors.OKBLUE}Tipo de mutacion: {bcolors.ENDC}{self.mutation_type.value}")
            print(f"{bcolors.OKBLUE}Probabilidad de mutacion: {bcolors.ENDC}{self.mutation_prob}")
            print(f"{bcolors.OKBLUE}Estrategia de seleccion para las nuevas poblaciones: {bcolors.ENDC}{self.selection_strategy.value}")
            print(f"{bcolors.OKBLUE}Tipo de seleccion de la nueva poblacion: {bcolors.ENDC}{self.gselection_type.value}")
            
        print()