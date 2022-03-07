"""
Modulo que contiene las clases encargadas de todas las opciones que puedan tener los demas modulos

"""

from .Tools import utilities, bcolors
from . import Enum, time, argparse, os

class MHType(Enum):
    """Tipos de Metaheristicas disponibles
    SA: Simulated Annealing
    GA: Genetic Algorithm
    LS: Local Search
    ILS: Iterated Local Search
    """
    SA = 'SA'
    GA = 'GA'
    LS = 'LS'
    ILS = 'ILS'

class TSPMove(Enum):
    """Tipos de movimientos disponibles para el TSP 
    TWO_OPT: Operador 2-opt
    THREE_OPT: Operador 3-opt
    SWAP: Operador swap
    """
    TWO_OPT = 'TWO_OPT'
    THREE_OPT = 'THREE_OPT'
    SWAP = 'SWAP'

""" S I M U L A T E D  A N N E A L I N G """

class InitialSolution(Enum):
    """ Metodos disponibles para crear una solución inicial
    RANDOM: Solución aleatoria
    NEAREST_N: Solución creada con la heuristica del vecino mas cercano
    DETERMINISTIC: Solución creada deterministicamente para testing, en este caso es secuencial
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

""" A L G O R I T M O   G E N E T I C O """

class SelectionType(Enum):
    """Tipos de selección de individuos
        RANDOM: Selección aleatoria
        BEST: Selección de los mejores (elitismo)
        ROULETTE: Selección proporcional al fitness
        TOURNAMENT: Selección de torneos k=3
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
    """Estrategias de selección de individuos de la población
    MU_LAMBDA: Estrategia (mu, lambda)
    MUPLUSLAMBDA: Estrategia (mu+lambda)
    """
    MULAMBDA = 'MULAMBDA'
    MUPLUSLAMBDA = 'MUPLUSLAMBDA'
    
""" L O C A L  S E A R C H  E  I T E R A T E D  L O C A L  S E A R C H """  
    
class PerturbationType(Enum):
    """Tipos de movimientos de perturbación para Iterated Local Search
    TWO_OPT: Operador 2-opt
    THREE_OPT: Operador 3-opt
    SWAP: Operador swap
    RANDOM: Operador aleatorio entre los anteriores
    """
    TWO_OPT = 'TWO_OPT'
    THREE_OPT = 'THREE_OPT'
    SWAP = 'SWAP'
    RANDOM = 'RANDOM'

class AlgorithmsOptions():
    """
    Clase para configurar y leer todas las opciones que pueda tener una metaheristica recibidas como atributo o como definiciones

    Attributes
    ----------
    output : str
        Archivo para imprimir la solución
    instance : str
        Archivo de la instancia TSP con formato TSPLib
    seed : int
        Semilla para el generador de números aleatorios
    metaheuristic : Enum
        Tipo de metaheurística a ejecutar SA o GA
    move : Enum
        Tipo del movimiento para la metaheurística
    max_evaluations : int
        Evaluaciones máximas 
    alpha : float
        Parámetro alfa para el enfriamiento de SA
    t0 : float
        Temperatura inicial para SA
    tmin : float
        Temperatura mínima para SA
    cooling : Enum
        Tipo de enfriamiento para SA
    pop_size : int
        Tamaño de la población 
    offspring_size : int
        Cantidad de hijos      
    pselection_type : Enum
        Selección de padres       
    crossover_type : Enum
        Cruzamiento
    mutation_type : Enum
        Mutacion
    mutation_prob : float
        Probabilidad de mutación
    selection_strategy : Enum
        Estrategia de selección de la nueva población
    gselection_type : Enum
        Selección de la nueva población
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
        Mostrar las opciones y parámetros finales
    """
    
    """ O P C I O N E S  G E N E R A L E S """
    
    solution = "output/solution.txt"	# Archivo para imprimir la solución

    trajectory = "output/trajectory.csv"	# Archivo para imprimir la trayectoria de solución
    
    instance = "instances/burma14.tsp" # Archivo de la instancia    
    
    seed = 0 # Semilla para el generador de número aleatorios    
     
    metaheuristic = MHType.SA # Tipo de metaheurística a ejecutar   
     
    move = TSPMove.TWO_OPT # Tipo del movimiento para la metaheurística o bien tipo de busqueda Local Search
    
    max_evaluations = 1000 # Evaluaciones máximas
    
    max_iterations = 20 # Numero de iteraciones máximas
    
    max_time = 60.0 # Tiempo de ejecucion máximo
    
    initial_solution = InitialSolution.RANDOM # Solución Inicial
    
    silent = False # Modo silencioso

    visualize = False # Visualizacion de la trayectoria

    replit = False # Si se esta ejecutando en Replit.com ya que causa inconveniencia con la graficacion

    verbose = False # modo verbose
    
    gui = False # modo Interfaz grafica
    
    """ O P C I O N E S  P A R A  S I M U L A T E D  A N N E A L I N G """
    
    alpha = 0.98 # Parámetro alfa para el enfriamiento
    
    t0 = 1000.0 # Temperatura inicial 
    
    tmin = 900.0 # Temperatura mínima    
    
    cooling = CoolingType.GEOMETRIC # Tipo de enfriamiento

    """ O P C I O N E S   P A R A   A L G O R I T M O   G E N E T I C O """
    
    pop_size = 10 # Cantidad de individuos de la población 
	
    offspring_size = 20 # Cantidad de hijos
    
    pselection_type = SelectionType.RANDOM # Selección de padres
    
    crossover_type = CrossoverType.OX # Cruzamiento
    
    mutation_type = TSPMove.SWAP # Mutacion
    
    mutation_prob = 0.2 # probabilidad de mutación 
    
    selection_strategy = SelectionStrategy.MULAMBDA # Estrategia de selección de la nueva población
    
    gselection_type = SelectionType.RANDOM # Selección de la nueva población
    
    """ O P C I O N E S   P A R A   L O C A L  S E A R C H  E  I T E R A T E D  L O C A L  S E A R C H """
    
    perturbation = PerturbationType.SWAP
    
    bestImprovement = False
    
    nPerturbations = 3

    def __init__(self, argv=[], **kwargs) -> None:

        # Semilla para el generador de números aleatorios
        self.seed = round(time.time() * 1000)
        
        # Leer argumentos que vengan por parametro o por definicion
        self.readOptions(argv, kwargs)

        # definir semilla para el generador aleatorio
        utilities.random.seed(self.seed)
        # Mostrar Opciones 
        #self.printOptions()
    

    def readOptions(self, argv: list, kwargs: dict) -> None:
        """ Leer las opciones introducidas como atributo y como definicion """
        # Si no se introdujeron argumentos
        if (len(argv) == 1 or not argv):
            print(f"{bcolors.WARNING}Warning: usando instancia por defecto: {self.instance} {bcolors.ENDC}")
            print(f"{bcolors.WARNING}Si desea utilizar otra instancia debe proporcionarla (use -i o --instance <file_path>) {bcolors.ENDC}")
            print(f"{bcolors.WARNING}Use el argumento '-h' o '--help' para mayor información {bcolors.ENDC}")
        
        parser = argparse.ArgumentParser()
        # Declarar y definir argumentos
        # Definir argumentos generales
        parser.add_argument("-s", "--silent", help="Ejecuta sin mostrar los cambios en cada ciclo de los algoritmos", action="store_true")
        parser.add_argument("-vi", "--visualize", help="Muestra la visualización de trayectoria a la mejor solución de forma grafica", action="store_true")
        parser.add_argument("-re", "--replit", help="Si se ejecuta en Replit.com ya que la visualización puede tener inconvenientes", action="store_true")
        parser.add_argument("-v", "--verbose", help="Ejecuta mostrando todos los detalles de cada iteración", action="store_true")
        parser.add_argument("-gui", "--gui", help="Ejecuta en modo interfaz grafica", action="store_true")

                
        parser.add_argument("-mh", "--metaheuristic", help="Tipo de Metaherisitica a usar:\n SA: Simulated Annealing\n GA: Genetic Algorithm\n LS: Local Search")
        parser.add_argument("-al", "--algorithm", help="Tipo de Algoritmo a usar:\n SA: Simulated Annealing\n GA: Genetic Algorithm\n LS: Local Search")
        parser.add_argument("-i", "--instance", help="Archivo con la instancia a utilizar en formato TSPLIB")
        parser.add_argument("-se", "--seed", help="Numero para ser usado como semilla para el generador de números aleatorios")
        parser.add_argument("-sol", "--solution", help="Nombre del archivo de salida para la solución y trayectoria")
        parser.add_argument("-mhm", "--move", help="Tipo de movimiento a utilizar en la heuristica [ 2opt | swap | 3opt ]")
        parser.add_argument("-e", "--evaluations", help="Numero máximo de soluciones a evaluar")
        parser.add_argument("-it", "--iterations", help="Numero máximo de iteraciones a realizar")
        parser.add_argument("-t", "--time", help="Limite de tiempo de ejecucion en segundos")

        # Definir argumentos de Simulated Annealing
        parser.add_argument("-is", "--insol", help="Solución inicial [ RANDOM | NEAREST_N | DETERMINISTIC ]")
        parser.add_argument("-a", "--alpha", help="Parámetro alfa para el esquema geometrico ]0,1]")
        parser.add_argument("-t0", "--tini", help="Temperatura inicial ]0,DOUBLE_MAX]")
        parser.add_argument("-tm", "--tmin", help="Temperatura mínima ]0,DOUBLE_MAX]")
        parser.add_argument("-c", "--cooling", help="Esquema de enfriamiento de la temperatura [ geometric | log | linear ]")

        # Definir argumentos de Algoritmo Genetico
        parser.add_argument("-p", "--psize", help="Cantidad de individuos de la población ]0,INT_MAX]")
        parser.add_argument("-o", "--osize", help="Cantidad de hijos a generar ]0,INT_MAX]")
        parser.add_argument("-ps", "--pselection", help="Operador de selección de padres [ random | best | roulette | tournament ]")
        parser.add_argument("-cr", "--crossover", help="Operador de crossover [ ox | opx | pmx ]")
        parser.add_argument("-mu", "--mutation", help="Operador de mutación [ swap | 2opt | 3opt ]")
        parser.add_argument("-mp", "--mprobability", help="Probabilidad de mutación [0.0,1.0]")
        parser.add_argument("-gs", "--gselection", help="Operador de selección de población [ random | best | roulette | tournament ]")
        parser.add_argument("-g", "--gstrategy", help="Estrategia de selección de padres [ mu,lambda | mu+lambda ]")
        
        # Definir argumentos de Local Search e Iterated Local Search
        parser.add_argument("-b", "--best", help="Ejecuta Local Search en modo best improvement", action="store_true")
        parser.add_argument("-per", "--perturbation", help="Tipo de perturbación a aplicar en ITS [ 2opt | swap | 3opt ]")
        parser.add_argument("-np", "--nperturbations", help="Cantidad de perturbaciones a aplicar en cada iteración de Iterated Local Search ]0,INT_MAX]")
        
        # Procesar argumentos
        args = parser.parse_args()

        # Procesar argumentos generales
        self.argsGeneral(args, kwargs)
        
        if self.metaheuristic == MHType.SA:
            # Procesar argumentos de Simulated Annealing
            self.argsSA(args, kwargs)
            # Validar logica de opciones
            if self.errorsSA():
                exit()
        elif self.metaheuristic == MHType.GA:
            # Procesar argumentos de Algoritmo Genetico
            self.argsGA(args, kwargs) 
            # Validar logica de opciones
            if self.errorsGA():
                exit()
        elif self.metaheuristic == MHType.LS or self.metaheuristic == MHType.ILS:
            # Procesar argumentos de Local Search e Iterated Local Search
            self.argsLS(args, kwargs)
        

    def argsGeneral(self, args: argparse.Namespace, kwargs: dict) -> None:
        """Procesar los argumentos generales, se pregunta se llego por argumento o por definicion, luego se asigna segun venga dando prioridad a los argumentos"""
        # Maximo tiempo de ejecucion 
        if (args.time or 'time' in kwargs):
            try:
                self.max_time = float(args.time) if args.time else float(kwargs['time'])
            except: 
                print(f"{bcolors.FAIL}Error: El tiempo máximo debe ser un número (-t | --time){bcolors.ENDC}")

        # Semilla 
        if (args.seed or 'seed' in kwargs):
            try:
                self.seed = int(args.seed) if args.seed else int(kwargs['seed'])
            except: 
                print(f"{bcolors.FAIL}Error: La semilla debe ser un número entero (-s | --seed){bcolors.ENDC}")

        # Archivo de salida para solución y trayectoria
        if (args.solution or 'solution' in kwargs):
            self.solution = args.solution if args.solution else kwargs['solution']
            self.trajectory = args.solution if args.solution else kwargs['solution']
            
            check = os.path.splitext(self.solution) # separa la ruta de la extension en lista
            if not check[1]:
                self.solution += '.txt'
                
            check = os.path.splitext(self.trajectory)
            if not check[1]:
                self.trajectory += '.csv'
                
        # Si se activa modo verbose
        if (args.verbose or 'verbose' in kwargs):
            self.verbose = args.verbose if args.verbose else kwargs['verbose']

        # Si se visualizara la trayectoria
        if (args.visualize or 'visualize' in kwargs):
            self.visualize = args.visualize if args.visualize else kwargs['visualize']
        
        # Si se activa el modo interfaz grafica
        if (args.gui or 'gui' in kwargs):
            self.gui = args.gui if args.gui else kwargs['gui']

        # Si se ejecuta en Replit.com
        if (args.replit or 'replit' in kwargs):
            self.replit = args.replit if args.replit else kwargs['replit']

        # Archivo de instancia
        if (args.instance or 'instance' in kwargs):
            self.instance = args.instance if args.instance else kwargs['instance']

        # Selección de Metaheuristica
        if (args.metaheuristic or 'metaheuristic' in kwargs):
            val = args.metaheuristic.upper() if args.metaheuristic else kwargs['metaheuristic'].upper()
            if (val == 'SA'):
                self.metaheuristic = MHType.SA
            elif (val == 'GA'):
                self.metaheuristic = MHType.GA
            elif (val == 'LS'):
                self.metaheuristic = MHType.LS
            elif (val == 'ILS'):
                self.metaheuristic = MHType.ILS
            else: print(f"{bcolors.FAIL}Error: Metaheuristica no reconocida (-mh | --metaheristic) {bcolors.ENDC}")  
        
        # Numero máximo de evaluaciones
        if (args.evaluations or 'evaluations' in kwargs):
            try:
                self.max_evaluations = int(args.evaluations) if args.evaluations else int(kwargs['evaluations'])
            except: 
                print(f"{bcolors.FAIL}Error: El número de evaluaciones debe ser un número entero (-e | --evaluations) {bcolors.ENDC}")

        # Numero máximo de iteraciones
        if (args.iterations or 'iterations' in kwargs):
            try:
                self.max_iterations = int(args.iterations) if args.iterations else int(kwargs['iterations'])
            except: 
                print(f"{bcolors.FAIL}Error: El número de iteraciones debe ser un número entero (-it | --iterations) {bcolors.ENDC}")

        # Selección del movimiento para la metaheurística
        if (args.move or 'move' in kwargs):
            val = args.move.lower() if args.move else kwargs['move'].lower()
            if (val == '2opt' or val == '2-opt'):
                self.move = TSPMove.TWO_OPT
            elif (val == '3opt' or val == '3-opt'):
                self.move = TSPMove.THREE_OPT
            elif (val == 'swap'):
                self.move = TSPMove.SWAP
            else: print(f"{bcolors.FAIL}Error: Tipo de movimiento no reconocido (-mhm | --move) {bcolors.ENDC}") 
            
        # Solución inicial
        if (args.insol or 'insol' in kwargs):
            val = args.insol.upper() if args.insol else kwargs['insol'].upper()
            if (val == 'RANDOM'):
                self.initial_solution = InitialSolution.RANDOM
            elif (val == 'NEAREST_N'):
                self.initial_solution = InitialSolution.NEAREST_N
            elif (val == 'DETERMINISTIC'):
                self.initial_solution = InitialSolution.DETERMINISTIC
            else: print(f"{bcolors.FAIL}Error: Opcion no reconocida en solución inicial (-is | --inso) {bcolors.ENDC}")

        # Modo de salida reducido para no mostrar todos los cambios en los ciclos de los algoritmos
        if (args.silent):
            self.silent = True


    def argsSA(self, args: argparse.Namespace, kwargs: dict) -> None:
        """Procesar los argumentos de Simulated Annealing"""

        # Selección del esquema de enfriamiento
        if (args.cooling or 'cooling' in kwargs):
            val = args.cooling.lower() if args.cooling else kwargs['cooling'].lower()
            if (val == 'geometric'):
                self.cooling = CoolingType.GEOMETRIC
            elif (val == 'log'):
                self.cooling = CoolingType.LOG
            elif (val == 'linear'):
                self.cooling = CoolingType.LINEAR    
            else: print(f"{bcolors.FAIL}Error: Opcion no reconocida en COOLING (-tc | --cooling) {bcolors.ENDC}")    

        # Parámetro alpha
        if (args.alpha or 'alpha' in kwargs):
            try:
                self.alpha = float(args.alpha) if args.alpha else float(kwargs['alpha'])
            except: 
                print(f"{bcolors.FAIL}Error: El valor de alpha debe ser un número en (-a | --alpha) {bcolors.ENDC}")
        
        # Temperatura inicial
        if (args.tini or 'tini' in kwargs):
            try:
                self.t0 = float(args.tini) if args.tini else float(kwargs['tini'])
            except:
                print(f"{bcolors.FAIL}Error: El valor de la temperatura inicial debe ser un número (-t0 | --tini) {bcolors.ENDC}")

        # Temperatura mínima
        if (args.tmin or 'tmin' in kwargs):
            try:
                self.tmin = float(args.tmin) if args.tmin else float(kwargs['tmin'])
            except:
                print(f"{bcolors.FAIL}Error: El valor de la temperatura mínima debe ser un número (-tmin | --tmin) {bcolors.ENDC}")


    def argsGA(self, args: argparse.Namespace, kwargs: dict) -> None:
        """Procesar los argumentos de Algoritmo Genetico"""
        # Cantidad de individuos de la población
        if (args.psize or 'psize' in kwargs):
            try:
                self.pop_size = int(args.psize) if args.psize else int(kwargs['psize'])
            except: 
                print(f"{bcolors.FAIL}Error: El tamaño de la población debe ser un número entero (-p | --psize){bcolors.ENDC}")

        # Cantidad de hijos a generar
        if (args.osize or 'osize' in kwargs):
            try:
                self.offspring_size = int(args.osize) if args.osize else int(kwargs['osize'])
            except: 
                print(f"{bcolors.FAIL}Error: La cantidad de hijos debe ser un número entero (-o | --osize){bcolors.ENDC}")

        # Selección de padres
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
            else: print(f"{bcolors.FAIL}Error: Opcion no reconocida en Selección de padres (-ps | --pselection) {bcolors.ENDC}")
        
        # Operador de Cruzamiento
        if (args.crossover or 'crossover' in kwargs):
            val = args.crossover.lower() if args.crossover else kwargs['crossover'].lower()
            if (val == 'ox'):
                self.crossover_type = CrossoverType.OX
            elif (val == 'opx'):
                self.crossover_type = CrossoverType.OPX
            elif (val == 'pmx'):
                self.crossover_type = CrossoverType.PMX
            else: print(f"{bcolors.FAIL}Error: Opcion no reconocida en Operador de Cruzamiento (-o | --crossover) {bcolors.ENDC}")

        # Operador de mutación
        if (args.mutation or 'mutation' in kwargs):
            val = args.mutation.lower() if args.mutation else kwargs['mutation'].lower()
            if (val == '2opt' or val == '2-opt'):
                self.mutation_type = TSPMove.TWO_OPT
            elif (val == '3opt' or val == '3-opt'):
                self.mutation_type = TSPMove.THREE_OPT
            elif (val == 'swap'):
                self.mutation_type = TSPMove.SWAP
            else: print(f"{bcolors.FAIL}Error: Tipo de mutación no reconocido (-mu | --mutation) {bcolors.ENDC}")

        # Probabilidad de mutación
        if (args.mprobability or 'mprobability' in kwargs):
            try:
                self.mutation_prob = float(args.mprobability) if args.mprobability else float(kwargs['mprobability'])
            except: 
                print(f"{bcolors.FAIL}Error: El valor de probabilidad de mutación debe ser un número en (-mp | --mprobability) {bcolors.ENDC}")
        
        # Operador de selección de población
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
            else: print(f"{bcolors.FAIL}Error: Opcion no reconocida en Selección de población (-gs | --gselection) {bcolors.ENDC}")

        # Estrategia de selección de padres
        if (args.gstrategy or 'gstrategy' in kwargs):
            val = args.gstrategy.lower() if args.gstrategy else kwargs['gstrategy'].lower()
            if (val == 'mu,lambda'):
                self.selection_strategy = SelectionStrategy.MULAMBDA
            elif (val == 'mu+lambda'):
                self.selection_strategy = SelectionStrategy.MUPLUSLAMBDA
            else: print(f"{bcolors.FAIL}Error: Tipo de selección de padres no reconocido (-g | --gstrategy) {bcolors.ENDC}")
            
            
    def argsLS(self, args: argparse.Namespace, kwargs: dict) -> None:
        """Procesar argumentos de Local Search"""
        
        # Selección del movimiento para la metaheurística
        if (args.perturbation or 'perturbation' in kwargs):
            val = args.perturbation.lower() if args.move else kwargs['perturbation'].lower()
            if (val == '2opt' or val == '2-opt'):
                self.perturbation = PerturbationType.TWO_OPT
            elif (val == '3opt' or val == '3-opt'):
                self.perturbation = PerturbationType.THREE_OPT
            elif (val == 'swap'):
                self.perturbation = PerturbationType.SWAP
            elif (val == 'random'):
                self.perturbation = PerturbationType.RANDOM
            else: print(f"{bcolors.FAIL}Error: Tipo de perturbación no reconocido (-per | --perturbation) {bcolors.ENDC}")
        
        # Si se ejecuta en Replit.com
        if (args.best or 'best' in kwargs):
            self.bestImprovement = args.best if args.best else kwargs['best']
        
        # Cantidad de hijos a generar
        if (args.nperturbations or 'nperturbations' in kwargs):
            try:
                self.nPerturbations = int(args.nperturbations) if args.nperturbations else int(kwargs['nperturbations'])
            except: 
                print(f"{bcolors.FAIL}Error: El número de perturbaciones debe ser un número entero (-np | --nperturbations){bcolors.ENDC}")


    def errorsSA(self) -> bool:
        """ Validar que algunos parámetros cumplan con la lógica del algoritmo a aplicar """
        error = False
        if (self.max_evaluations <= 0 or self.max_iterations <= 0):
            print(f"{bcolors.FAIL}Error: iteraciones o evaluaciones máximas deben ser > 0 Iteraciones: {self.max_iterations} Evaluaciones: {self.max_evaluations}{bcolors.ENDC}")
            error = True
        if (self.tmin <= 0 or self.t0 <= 0):
            print(f"{bcolors.FAIL}Error: Las temperatura mínima y la temperatura inicial máximas deben ser > 0, tmin: {self.tmin} t0: {self.t0} evaluaciones: {self.max_evaluations} {bcolors.ENDC}")
            error = True
        if (self.alpha <= 0 or self.alpha > 1):
            print(f"{bcolors.FAIL}Error: alfa debe ser > 0 y <= 1, valor: {self.alpha} (-a | --alpha){bcolors.ENDC}")
            error = True
        if (self.t0 <= self.tmin):
            print(f"{bcolors.FAIL}Error: t0 debe ser > tmin, valor tmin: {self.tmin} valor t0: {self.t0} (-t0 | --tini y -tm | --tmin){bcolors.ENDC}")
            error = True
        return error
    
    def errorsGA(self) -> bool:
        """ Validar que algunos parámetros cumplan con la logica del algoritmo a aplicar """
        error = False
        if (self.max_evaluations <= 0 or self.max_iterations <= 0):
            print(f"{bcolors.FAIL}Error: iteraciones o evaluaciones máximas deben ser > 0 Iteraciones: {self.max_iterations} Evaluaciones: {self.max_evaluations}{bcolors.ENDC}")
            error = True
        if (self.mutation_prob > 1.0 or self.mutation_prob < 0.0 ):
            print(f"{bcolors.FAIL}Error: La probabilidad de mutación debe ser [0.0, 1.0]: {self.mutation_prob}{bcolors.ENDC}")
            error = True
        if (self.selection_strategy == SelectionStrategy.MULAMBDA and self.pop_size > self.offspring_size):
            print(f"{bcolors.FAIL}Error: En (mu,lambda) la población (-p | --psize) debe ser >= que los hijos (-o | --osize){bcolors.ENDC}")
            error = True
        if (self.pop_size <= 1):
            print(f"{bcolors.FAIL}Error: La cantidad de individuos de la población (-p | --psize) debe ser > 1{bcolors.ENDC}")
            error = True     
        return error
    
    
    def errors(self) -> bool:
        """ Devuelve verdadero si hay errores en las configuraciones del metodo de busqueda """
        if self.metaheuristic == MHType.SA:
            return self.errorsSA()
        elif self.metaheuristic == MHType.GA:
            return self.errorsGA()
        return False
    
    
    def printOptions(self) -> None:
        """ Mostrar las opciones y parámetros finales """
        # Opciones generales
        print(f"{bcolors.HEADER}\n\t\tOPCIONES GENERALES\n {bcolors.ENDC}")        
        print(f"{bcolors.OKBLUE}Archivo de instancia: {bcolors.ENDC}{self.instance}")
        print(f"{bcolors.OKBLUE}Archivo para imprimir la solución: {bcolors.ENDC}{self.solution}")
        print(f"{bcolors.OKBLUE}Tipo de metaheurística a ejecutar: {bcolors.ENDC}{self.metaheuristic.value}")
        print(f"{bcolors.OKBLUE}Tipo del movimiento para la metaheurística: {bcolors.ENDC}{self.move.value}")
        print(f"{bcolors.OKBLUE}Semilla para el generador de números aleatorios: {bcolors.ENDC}{self.seed}")
        print(f"{bcolors.OKBLUE}Evaluaciones máximas: {bcolors.ENDC}{self.max_evaluations}")
        print(f"{bcolors.OKBLUE}Iteraciones máximas: {bcolors.ENDC}{self.max_iterations}")
        print(f"{bcolors.OKBLUE}Solución Inicial: {bcolors.ENDC}{self.initial_solution.value}")
        print(f"{bcolors.OKBLUE}Límite de tiempo de ejecución: {bcolors.ENDC}{self.max_time} segundos")

        # Opciones para Simulated Annealing
        if (self.metaheuristic == MHType.SA):
            print(f"{bcolors.HEADER}\n\t\tOPCIONES PARA SIMULATED ANNEALING\n {bcolors.ENDC}")        
            print(f"{bcolors.OKBLUE}Parámetro alfa para el enfriamiento: {bcolors.ENDC}{self.alpha}")
            print(f"{bcolors.OKBLUE}Temperatura inicial: {bcolors.ENDC}{self.t0}")
            print(f"{bcolors.OKBLUE}Temperatura mínima: {bcolors.ENDC}{self.tmin}")
            print(f"{bcolors.OKBLUE}Tipo de enfriamiento: {bcolors.ENDC}{self.cooling.value}")
        elif (self.metaheuristic == MHType.GA): # Opciones para Algoritmo Genetico
            print(f"{bcolors.HEADER}\n\t\tOPCIONES PARA ALGORITMO GENÉTICO\n {bcolors.ENDC}")        
            print(f"{bcolors.OKBLUE}Cantidad de individuos de la población: {bcolors.ENDC}{self.pop_size}")
            print(f"{bcolors.OKBLUE}Cantidad de hijos: {bcolors.ENDC}{self.offspring_size}")
            print(f"{bcolors.OKBLUE}Selección de padres: {bcolors.ENDC}{self.pselection_type.value}")
            print(f"{bcolors.OKBLUE}Tipo de cruzamiento: {bcolors.ENDC}{self.crossover_type.value}")
            print(f"{bcolors.OKBLUE}Tipo de mutación: {bcolors.ENDC}{self.mutation_type.value}")
            print(f"{bcolors.OKBLUE}Probabilidad de mutación: {bcolors.ENDC}{self.mutation_prob}")
            print(f"{bcolors.OKBLUE}Estrategia de selección para las nuevas poblaciones: {bcolors.ENDC}{self.selection_strategy.value}")
            print(f"{bcolors.OKBLUE}Tipo de selección de la nueva población: {bcolors.ENDC}{self.gselection_type.value}")
        elif (self.metaheuristic == MHType.LS or self.metaheuristic == MHType.ILS):
            print(f"{bcolors.HEADER}\n\t\tOPCIONES PARA LOCAL SEARCH E ITERATED LOCAL SEARCH\n {bcolors.ENDC}")        
            print(f"{bcolors.OKBLUE}Tipo de movimiento para búsqueda: {bcolors.ENDC}{self.move.value}")
            print(f"{bcolors.OKBLUE}Best Improvement: {bcolors.ENDC}{self.bestImprovement}")
            print(f"{bcolors.OKBLUE}Tipo de perturbación para búsqueda ILS: {bcolors.ENDC}{self.perturbation.value}")
            print(f"{bcolors.OKBLUE}Número de perturbaciones a aplicar para búsqueda ILS: {bcolors.ENDC}{self.nPerturbations}")
        
                        
        print()