from enum import Enum
from src.SimulatedAnnealing.SimulatedAnnealing import SimulatedAnnealing
from src.Utilities import bcolors
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

class AlgorithmsOptions():
    
    # Archivo para imprimir la solucion
    output = "solucion.txt";
	
    # Archivo de la instancia 
    filename = "instances/burma14.tsp";
    
    # Semilla para el generador de numero aleatorios 
    seed = 0;
    
    # Tipo de metaheuristica a ejecutar 
    metaheuristic = MHType.SA;
    
    # Tipo del movimiento para la metaheuristica 
    mh_move = TSPMove.SWAP;
    
    # Parametro alfa para el enfriamiento geometrico
    alpha = 0.98;
    
    # Temperatura inicial 
    t0 = 1000.0;
    
    # Temperatura minima 
    t_min = 900.0;
    
    # Evaluaciones maximas
    max_evaluations = 1000;

    # Tipo de enfriamiento
    cooling = SimulatedAnnealing.CoolingType.GEOMETRIC;

    def __init__(self, argv, **kwargs) -> None:

        # Semilla para el generador de numeros aleatorios
        seed = round(time.time() * 1000)
        print(argv)
        # Leer argumentos
        self.readOptions(argv)
    

    def readOptions(self, argv) -> None:
        if (len(argv) == 1):
            print(f"{bcolors.WARNING}Warning: usando instancia por defecto: {self.filename} {bcolors.ENDC}")
            print(f"{bcolors.WARNING}Si desea utilizar otra instancia debe proporcionarla (use -i o --instance <file_path>) {bcolors.ENDC}")
            print(f"{bcolors.WARNING}Use el argumento '-h' o '--help' para mayor informacion {bcolors.ENDC}")
        
        parser = argparse.ArgumentParser()
        # Declarar y definir argumentos
        parser.add_argument("-v", "--verbose", help="Mostrar información de depuración", action="store_true")
        parser.add_argument("-mh", "--metaheuristic", help="Tipo de Metaherisitica a usar:\n SA: Simulated Annealing\n GA: Genetic Algorithm")
        parser.add_argument("-i", "--instance", help="Archivo con la instancia a utilizar en formato TSPLIB")
        parser.add_argument("-mhm", "--move", help="Tipo de movimiento a utilizar en la heristica [ 2opt | swap ]")
        parser.add_argument("-tc", "--cooling", help="Esquema de enfriamiento de la temperatura [ geometric | log | linear ]")
        parser.add_argument("-a", "--alpha", help="Parametro alfa para el esquema geometrico ]0,1]")
        parser.add_argument("-t0", "--t0", help="Temperatura inicial ]0,DOUBLE_MAX]")
        parser.add_argument("-tmin", "--tmin", help="Temperatura minima ]0,DOUBLE_MAX]")
        parser.add_argument("-e", "--evaluations", help="Numero maximo de soluciones a evaluar")
        parser.add_argument("-s", "--seed", help="Numero para ser usado como semilla para el generador de numeros aleatorios")
        parser.add_argument("-o", "--output", help="Nombre del archivo de salida para la solucion")


        args = parser.parse_args()

        # Procesar los argumentos
        if args.verbose:
            print ("depuración activada!!!")

        # Semilla 
        if args.seed:
            self.seed = int(args.seed)

        # Archivo de salida
        if args.output:
            self.output = args.output  

        # Archivo de instancia
        if args.instance:
            self.instance = args.instance  

        # Seleccion de Metaheristica
        if args.metaheuristic:
            val = args.metaheuristic.upper()
            if val == 'SA':
                self.metaheuristic = MHType.SA
            elif val == 'GA':
                self.metaheuristic = MHType.GA
            else: print(f"{bcolors.FAIL}Error: opcion no reconocida -mh {bcolors.ENDC}")  

        # Seleccion del movimiento para la metaheristica
        if args.move:
            val = args.move.lower()
            if val == '2opt':
                self.move = TSPMove.TWO_OPT
            elif val == 'swap':
                self.move = TSPMove.SWAP
            else: print(f"{bcolors.FAIL}Error: Movimiento no reconocido -mhm {bcolors.ENDC}")

        # Seleccion del esquema de enfriamiento
        if args.cooling:
            val = args.cooling.lower()
            if val == 'geometric':
                self.cooling = SimulatedAnnealing.CoolingType.GEOMETRIC
            elif val == 'log':
                self.cooling = SimulatedAnnealing.CoolingType.LOG
            elif val == 'linear':
                self.cooling = SimulatedAnnealing.CoolingType.LINEAR    
            else: print(f"{bcolors.FAIL}Error: opcion no reconocida -tc {bcolors.ENDC}")    

        # Parametro alpha
        if args.alpha:
            self.alpha = float(args.alpha)
        
        # Temperatura inicial
        if args.t0:
            self.t0 = float(args.t0)

        # Temperatura inicial
        if args.tmin:
            self.tmin = float(args.tmin)

        # Numero maximo de evaluaciones
        if args.evaluations:
            self.evaluations = int(args.evaluations)

        self.validateOptions()
        

    def validateOptions(self) -> None:
        """ Validar que algunos paramaetros para los algotimos sean coerentes"""
        
        if (self.max_evaluations <= 0 and self.t_min <= 0):
            print(f"{bcolors.FAIL}Error: temperatura minima o evaluaciones maximas deben ser > 0, valor: {self.max_evaluations} {bcolors.ENDC}")
        if (self.alpha <= 0 or self.alpha > 1):
            print(f"{bcolors.FAIL}Error: alfa debe ser > 0 y <= 1, valor: {self.alpha} {bcolors.ENDC}")
        if (self.t0 <= 0):
            print(f"{bcolors.FAIL}Error: t0 debe ser > 0 , valor:  {self.t0} {bcolors.ENDC}")
