# Framework para resolver TSP
Framework para resolver el problema del vendedor viajero aplicando algoritmos metaheuristicos como el Simulated Annealing o Genetic Algorithm
**Versión de prueba, ejecutar python tspf.py + los argumentos a utilizar definidos abajo**
## Contenido
* <b>código</b>: codigo en lenguaje Python en la carpeta src/ para ser preparado y distribuido como paquete Python

* <b>instancias</b>: instancias en formato TSPlib en la carpeta instances/

## Descripción

General

* **TSPlibReader.py:** Clase que implementa funciones para leer las instancias de TSP en el formato de la librería de instancias TSPlib.

* **TSP.py:** Clase que representa la instancia de TSP. Contiene los siguientes métodos:

	* **compute_tour_length:** Calcula el costo de un tour

	* **tsp_check_tour:** Revisa si un tour es correcto

	* **random_tour:** Genera un tour aleatorio

	* **greedy_nearest_n:** Genera un tour utilizando la heurística del vecino más cercano

* **Tour.py:** Clase que implementa una solución del TSP. El constructor de clase permite definir si la solución inicial es construída aleatoriamente, utilizando la heurística del vecino más cercano o una solución secuencial. Contiene las siguientes variables y métodos:

	* **current:** Solución del TSP que se representa con un arreglo de enteros de tamaño n+1, donde n son los nodos (ciudades) y la última ciudad del tour corresponde siempre a la primera ciudad. 

	* **cost:** Costo del tour de la solución

	* **swap**: Método que aplica el movimiento swap a dos nodos en el tour actual

	* **twoOptSwap:** Método que aplica el movimiento 2-opt a dos nodos en el tour actual

	* **randomNeighbor:** Método que aplica aleatoriamente a dos nodos el movimiento definido en move_type (TSPMove.TWO_OPT o TSPMove.SWAP)

  
* **Main.py:** Clase principal que ejecuta el software
 

* **AlgorithmsOptions.py:** Clase que configura y lee todos los argumentos que puedan tener uno de los algoritmos a aplicar

Algoritmos

* **SimulatedAnnealing.py:** Clase que implementa el método de búsqueda de Simulated Annealing

	* **search:** Método que inicia la búsqueda de Simulated Annealing comenzando de una solución inicial

	* **terminationCondition:** Método que revisa si la condición de término (temperatura mínima o número de evaluaciones) se ha cumplido

	* **getAcceptanceProbability:** Método que calcula la probabilidad de aceptar una solución

	* **reduceTemperature:** Método que reduce el valor de la temperatura siguiendo un esquema de enfriamiento seleccionado
  

## Argumentos

Las opciones de los algoritmos se pueden cambiar en la clase AlgorithmsOptions.py, sin embargo, al crear la clase se le pueden entregar definiciones de las variables a definir, como por ejemplo: "options = AlgorithmsOptions(seed=98849,...)". O bien, si se es ejecutado directamente desde la línea de comando se le pueden pasar los siguientes argumentos:

Argumentos Generales:
  
* **Metaheuristica:** Tipo de Metaherisitica a usar, por defecto SA
	*  **SA:** Simulated Annealing 
	* **GA:** Genetic Algorithm.
	*  (-mh o --metaheuristic). **Ejemplo:** python tspf.py -mh SA

* **Instancia:** Ruta al archivo de la instancia de TSP a resolver, por defecto instances/burma14.tsp.
	*  (-i o --instance **ruta**). **Ejemplo:** python tspf.py -i hola.tsp
  

* **Semilla**: Semilla para el generador de números aleatorios y todo los relacionado al modulo random de Python.
	*  (-s o --seed **entero**). **Ejemplo:** python tspf.py -s 4854

* **Movimiento:** Tipo de movimiento en formato TSPMove que se utilizará para la ejecución. Los valores posibles son TSPMove.SWAP y TSPMove.TWO_OPT, por defecto se utiliza swap. 
	* (-mhm o --move **[ swap | 2opt ]**). **Ejemplo:** python tspf.py --move 2opt
	
* **Evaluaciones:** Número máximo de funciones de evaluación calculadas, por defecto se utiliza 1000
	 * (-e o --evaluations **entero**). **Ejemplo:** python tspf.py -e 2000
	 
* **Solución Inicial:** Tipo de solución inicial en formato InitialSolution que se utilizarácución. Los valores posibles son InitialSolution.RANDOM, InitialSolution.NEAREST_N y InitialSolution.DETERMINISTIC, por defecto se utiliza random. 
	* (-is o --insol **[ random | nearest_n | deterministic ]**). **Ejemplo:** python tspf.py --insol deterministic

Argumentos para Simulated Annealing:

* **Enfriamiento:** Variable del tipo CoolingType que indica el tipo de esquema de enfriamiento que se utilizará para la ejecución de Simulated Annealing. Los valores posibles son CoolingType.GEOMETRIC, CoolingType.LOG y CoolingType.LINEAR, por defecto geometric.

	* (-c o --cooling **[ linear | geometric | log ]**). **Ejemplo:** python tspf.py -c linear

* **Alfa:** Valor del parámetro alpha para el enfriamiento lineal, por defecto 0.98.

	* (-a o --alpha **]0,1]**). **Ejemplo:** python tspf.py -a 0.3
  

* **Temperatura Inicial:** Valor de la temperatura inicial t0, por defecto 1000.0. 
	* (-t0 o --tini **]0,FLOAT_MAX]**). **Ejemplo:** python tspf.py -t0 956.45

* **Temperatura Mínima:** Valor de la temperatura mínima, por defecto 900.0.
	*  (-tmin o --tmin **]0,FLOAT_MAX]**). **Ejemplo:** python tspf.py -tmin 800.87
