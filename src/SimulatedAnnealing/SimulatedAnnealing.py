from enum import Enum

class CoolingType(Enum):
    """Esquemas de enfriamiento disponibles 

    GEOMETRIC: t = t * alpha
    LINEAR: t = t * (1 - (evaluation / max_evaluations))
    LOG: t = t * alpha * 1/ln(evaluation + 1)
    """
    GEOMETRIC = 'GEOMETRIC'
    LINEAR = 'LINEAR'
    LOG = 'LOG'

class SimulatedAnnealing():



    def __init__(self) -> None:
        pass