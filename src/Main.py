from src.Tour import Tour
from src.AlgorithmsOptions import AlgorithmsOptions, MHType
from src.TSP import TSP
import sys


class Main():
    """
    Clase principal que implementa algoritmos metaheristicos para resolver el problema del vendedor viajero (TSP)

    Methods
    -------
    __init__(argv=sys.argv)
        Clase principal que recibe los argumentos que puedan haber sido incluidos al ejecutar el script en la consola
    """
    def __init__(self, argv=sys.argv) -> None:
        """
        Clase principal que recibe los argumentos que puedan haber sido incluidos al ejecutar el script en la consola

        Parameters
        ----------
        argv : list of str, optional
            Lista con los argumentos que pueda tener al inicializar la clase

        """
        
        # leer e inicializar las opciones 
        opciones = AlgorithmsOptions(argv)

        # leer e interpretar el problema TSP leido desde la instancia definida
        problema = TSP(opciones)

        solucion_inicial = Tour(sol_inicial=opciones.initial_solution, problema=problema)
        print(solucion_inicial.actual, solucion_inicial.costo)
     