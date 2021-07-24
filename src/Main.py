from enum import Enum
from src.AlgorithmsOptions import AlgorithmsOptions
import sys

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

class Main():
    """
    Clase principal que implementa algoritmos metaheristicos para resolver el problema del vendedor viajero (TSP)

    ...
    
    Attributes
    ----------
    Methods
    -------
    __init__(argv=sys.argv)
        Constructor que recibe los argumentos que puedan haber sido incluidos al ejecutar el script en la consola
    """
    def __init__(self, argv=sys.argv) -> None:
        """
        Constructor que recibe los argumentos que puedan haber sido incluidos al ejecutar el script en la consola

        ...

        Parameters
        ----------
        argv : list of str, optional
            Lista con los argumentos que pueda tener al inicializar la clase

        """
        opciones = AlgorithmsOptions(argv)
        