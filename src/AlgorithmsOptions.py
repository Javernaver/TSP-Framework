from src.Main import MHType, TSPMove


class AlgorithmsOptions():
    
    # archivo para imprimir la solucion
    output = "solucion.txt";
	
    # archivo de la instancia 
    filename = "instances/burma14.tsp";
    
    # semilla para el generador de numero aleatorios 
    seed = 0;
    
    # tipo de metaheuristica a ejecutar 
    metaheuristic = MHType.SA;
    
    # tipo del movimiento para la metaheuristica 
    mh_move = TSPMove.SWAP;
    
    # parametro alfa para el enfriamiento geometrico
    alpha = 0.98;
    
    # temperatura inicial 
    t0 = 1000.0;
    
    # temperatura minima 
    t_min = 900.0;
    
    # evaluaciones maximas
    max_evaluations = 1000;


    def __init__(self, argv) -> None:
        print(argv)