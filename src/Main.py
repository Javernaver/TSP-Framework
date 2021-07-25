from src.AlgorithmsOptions import AlgorithmsOptions, MHType
import sys


class Main():
    """
    Clase principal que implementa algoritmos metaheristicos para resolver el problema del vendedor viajero (TSP)

    Attributes
    ----------
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
        opciones = AlgorithmsOptions(argv)
        