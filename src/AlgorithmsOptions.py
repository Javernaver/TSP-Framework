from enum import Enum
from src.Utilities import bcolors
import src.Utilities as util
import time
import argparse

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
    """Esquemas de enfriamiento disponibles 

    GEOMETRIC: t = t * alpha
    LINEAR: t = t * (1 - (evaluation / max_evaluations))
    LOG: t = t * alpha * 1/ln(evaluation + 1)
    """
    GEOMETRIC = 'GEOMETRIC'
    LINEAR = 'LINEAR'
    LOG = 'LOG'

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

    Methods
    -------
    __init__(args, **keyargs)
        Clase para configurar y leer todas las opciones que pueda tener una metaheristica recibidas como atributo
    readOptions(argv, keyargs)
        Clase que lee las opciones introducidas como atributo y por definicion
    validateOptions()
        Validar que algunos paramaetros para los algoritmos sean coerentes
    """
    
    # OPCIONES GENERALES
    # Archivo para imprimir la solucion
    output = "solucion.txt";
	
    # Archivo de la instancia 
    instance = "instances/burma14.tsp";
    
    # Semilla para el generador de numero aleatorios 
    seed = 0;
    
    # Tipo de metaheuristica a ejecutar 
    metaheuristic = MHType.SA;
    
    # Tipo del movimiento para la metaheuristica 
    move = TSPMove.SWAP;

    # Evaluaciones maximas
    max_evaluations = 1000;

    # Solucion Inicial
    initial_solution = InitialSolution.RANDOM
    
    # OPCIONES PARA SIMULATED ANNEALING 
    # Parametro alfa para el enfriamiento
    alpha = 0.98;
    
    # Temperatura inicial 
    t0 = 1000.0;
    
    # Temperatura minima 
    tmin = 900.0;
    
    # Tipo de enfriamiento
    cooling = CoolingType.GEOMETRIC;

    def __init__(self, argv=[], **kwargs) -> None:

        # Semilla para el generador de numeros aleatorios
        self.seed = round(time.time() * 1000)
        
        # Leer argumentos que vengan por parametro o por definicion
        self.readOptions(argv, kwargs)

        # Setear semilla en el generador de numeros aleatorio
        util.seed = self.seed
        # definir semilla para el generador aleatorio
        util.random.seed(self.seed)
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
        # Argumentos generales
        parser.add_argument("-mh", "--metaheuristic", help="Tipo de Metaherisitica a usar:\n SA: Simulated Annealing\n GA: Genetic Algorithm")
        parser.add_argument("-i", "--instance", help="Archivo con la instancia a utilizar en formato TSPLIB")
        parser.add_argument("-s", "--seed", help="Numero para ser usado como semilla para el generador de numeros aleatorios")
        parser.add_argument("-o", "--output", help="Nombre del archivo de salida para la solucion")
        parser.add_argument("-mhm", "--move", help="Tipo de movimiento a utilizar en la heuristica [ 2opt | swap ]")
        parser.add_argument("-e", "--evaluations", help="Numero maximo de soluciones a evaluar")
        parser.add_argument("-is", "--insol", help="Solucion inicial [ RANDOM | NEAREST_N | DETERMINISTIC ]")

        # Argumentos de Simulated Annealing
        parser.add_argument("-a", "--alpha", help="Parametro alfa para el esquema geometrico ]0,1]")
        parser.add_argument("-t0", "--tini", help="Temperatura inicial ]0,DOUBLE_MAX]")
        parser.add_argument("-tmin", "--tmin", help="Temperatura minima ]0,DOUBLE_MAX]")
        parser.add_argument("-tc", "--cooling", help="Esquema de enfriamiento de la temperatura [ geometric | log | linear ]")


        args = parser.parse_args()

        # Procesar los argumentos generales, se pregunta se llego por argumento o por definicion, luego se asigna segun venga dando prioridad a los argumentos
        # Semilla 
        if (args.seed or 'seed' in kwargs):
            try:
                self.seed = int(args.seed) if args.seed else int(kwargs['seed'])
            except: 
                print(f"{bcolors.FAIL}Error: La semilla debe ser un numero entero (-s o --seed){bcolors.ENDC}")

        # Archivo de salida
        if (args.output or 'output' in kwargs):
            self.output = args.output if args.output else kwargs['output']

        # Archivo de instancia
        if (args.instance or 'instance' in kwargs):
            self.instance = args.instance if args.instance else kwargs['instance']

        # Seleccion de Metaheristica
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
                self.evaluations = int(args.evaluations) if args.evaluations else int(kwargs['evaluations'])
            except: 
                print(f"{bcolors.FAIL}Error: El numero de evaluaciones debe ser un numero entero (-e o --evaluations) {bcolors.ENDC}")

        # Seleccion del movimiento para la metaheuristica
        if (args.move or 'move' in kwargs):
            val = args.move.lower() if args.move else kwargs['move'].lower()
            if (val == '2opt'):
                self.move = TSPMove.TWO_OPT
            elif (val == 'swap'):
                self.move = TSPMove.SWAP
            else: print(f"{bcolors.FAIL}Error: Tipo de movimiento no reconocido (-mhm o --move) {bcolors.ENDC}")

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


        # Procesar los argumentos de Simulated Annealing
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

        # Validar logica de opciones
        self.validateOptions()
        

    def validateOptions(self) -> None:
        """ Validar que algunos parametros cumplan con la logica del algoritmo a aplicar """
        
        if (self.max_evaluations <= 0 or self.tmin <= 0 or self.t0 <= 0):
            print(f"{bcolors.FAIL}Error: Las temperatura minima, la temperatura inicial y las evaluaciones maximas deben ser > 0, tmin: {self.tmin} t0: {self.t0} evaluaciones: {self.max_evaluations} {bcolors.ENDC}")
            exit()
        if (self.alpha <= 0 or self.alpha > 1):
            print(f"{bcolors.FAIL}Error: alfa debe ser > 0 y <= 1, valor: {self.alpha} {bcolors.ENDC}")
            exit()
        if (self.t0 <= self.tmin):
            print(f"{bcolors.FAIL}Error: t0 debe ser > tmin, valor tmin: {self.tmin} valor t0: {self.t0}{bcolors.ENDC}")
            exit()

                   
    def printOptions(self) -> None:
        """ Mostrar las opciones finales al inicializar la clase """

        # Opciones generales
        print(f"{bcolors.HEADER}\n\t\tOPCIONES GENERALES\n {bcolors.ENDC}")        
        print(f"{bcolors.OKBLUE}Archivo de instancia: {bcolors.ENDC}{self.instance}")
        print(f"{bcolors.OKBLUE}Archivo para imprimir la solucion: {bcolors.ENDC}{self.output}")
        print(f"{bcolors.OKBLUE}Tipo de metaheuristica a ejecutar: {bcolors.ENDC}{self.metaheuristic.value}")
        print(f"{bcolors.OKBLUE}Tipo del movimiento para la metaheuristica: {bcolors.ENDC}{self.move.value}")
        print(f"{bcolors.OKBLUE}Semilla para el generador de numero aleatorios: {bcolors.ENDC}{self.seed}")
        print(f"{bcolors.OKBLUE}Evaluaciones maximas: {bcolors.ENDC}{self.max_evaluations}")
        print(f"{bcolors.OKBLUE}Solucion Inicial: {bcolors.ENDC}{self.initial_solution.value}")

        # Opciones para Simulated Annealing
        if (self.metaheuristic == MHType.SA):
            print(f"{bcolors.HEADER}\n\t\tOPCIONES PARA SIMULATED ANNEALING\n {bcolors.ENDC}")        
            print(f"{bcolors.OKBLUE}Parametro alfa para el enfriamiento: {bcolors.ENDC}{self.alpha}")
            print(f"{bcolors.OKBLUE}Temperatura inicial: {bcolors.ENDC}{self.t0}")
            print(f"{bcolors.OKBLUE}Temperatura minima: {bcolors.ENDC}{self.tmin}")
            print(f"{bcolors.OKBLUE}Tipo de enfriamiento: {bcolors.ENDC}{self.cooling.value}")
