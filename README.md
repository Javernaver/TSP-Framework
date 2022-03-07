# Framework de algoritmos para resolver el Problema del Vendedor Viajero
Framework para resolver el problema del vendedor viajero aplicando algoritmos de búsqueda  como el Simulated Annealing, Algoritmo Genético, Local Search e Iterated Local Search.

**Visualización**:
<p align="center">
<img src="https://media.giphy.com/media/uLzy84eyEANxqK83Iw/giphy.gif"/>
</p>

**GUI**:
<p align="center">
<img src="https://media.giphy.com/media/7I1c3ms9OekiCkcbQD/giphy.gif"/>
</p>

## Contenido
* **código fuente:** código en lenguaje Python en la carpeta tspf/ para ser preparado y distribuido como paquete Python

* **instancias:** instancias en formato TSPlib en la carpeta instances/

## Uso sin instalación (Recomendado)

Para ejecutar de forma local, puede descargar el repositorio e instalar los requerimientos abriendo una terminal dentro de la carpeta del proyecto y luego ejecutar:
```sh
pip install -r requirements.txt
```

Luego, ejecutar python (python3 en Linux) tspf.py + los argumentos a utilizar definidos  desde la carpeta donde tenga el framework
```sh
python tspf.py --instance instances/burma14.tsp
```

## Instalación como script Python

El framework puede instalarse como paquete desde PyPi (https://pypi.org/project/TSP-Framework/) o GitHub, para esto utilice:

```sh
pip install TSP-Framework
```
o
```sh
pip install git+https://github.com/Javernaver/TSP-Framework.git
```
Una vez instalado tendrá acceso al comando **tspf** el cual podrá ser utilizado desde cualquier directorio. Recuerde que para utilizar estos comandos debe tener el directorio en las variables de entorno o PATH del sistema operativo.
### Importante sobre comando tspf
Al utilizar el comando **tspf** debe agregar igualmente el parámetro con la instancia, ya que de otro modo no funcionara la instancia por defecto, debe utilizar una con el parámetro -i o --instance <PATH> al archivo en formato TSPlib (http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/). Ejemplo de uso:

```sh
tspf --instance archivo.tsp
```

## Uso Online con Replit

Puede utilizar el framework de forma online con Replit: https://replit.com/@Javernaver/TSP-Framework
Se recomienda tener una cuenta en Replit y hacer fork del proyecto para una mejor experiencia y edición del código fuente.

## Descripción

### General

* **TSPlibReader.py:** Modulo con la clase que implementa funciones para leer las instancias de TSP en el formato de la librería de instancias TSPlib.

* **Tsp.py:** Modulo con la clase que representa la instancia de TSP. Contiene los siguientes métodos:

	* **compute_tour_length:** Calcula el costo de un tour

	* **tsp_check_tour:** Revisa si un tour es correcto

	* **random_tour:** Genera un tour aleatorio

	* **greedy_nearest_n:** Genera un tour utilizando la heurística del vecino más cercano

* **Tour.py:** Modulo con la clase que implementa una solución del TSP. El constructor de clase permite definir si la solución inicial es construida aleatoriamente, utilizando la heurística del vecino más cercano o una solución secuencial. Contiene las siguientes variables y métodos:

	* **current:** Solución del TSP que se representa con un arreglo de enteros de tamaño n+1, donde n son los nodos (ciudades) y la última ciudad del tour corresponde siempre a la primera ciudad. 

	* **cost:** Costo del tour de la solución

	* **swap**: Método que aplica el movimiento swap a dos nodos en el tour actual

	* **twoOptSwap:** Método que aplica el movimiento 2-opt a dos nodos en el tour actual

	* **randomNeighbor:** Método que aplica aleatoriamente a dos nodos el movimiento definido en move_type (TSPMove.TWO_OPT o TSPMove.SWAP)

  
* **main.py:** Modulo principal que ejecuta el software uniendo todos los demás módulos
 

* **AlgorithmsOptions.py:** Modulo con la clase que configura y lee todos los argumentos que puedan tener uno de los algoritmos a aplicar
 
* **utilities.py:** Modulo distintas utilidades utilizadas por los demás módulos

* **plot.py:** Modulo encargado de generar y mostrar los distintos gráficos utilizados como los generados en la trayectoria de las soluciones 

* **gui.py:** Modulo encargado de generar y mostrar la interfaz gráfica de usuario 

### Algoritmos

* **SimulatedAnnealing.py:** Modulo con la clase que implementa el método de búsqueda de Simulated Annealing

	* **search:** Método que inicia la búsqueda de Simulated Annealing comenzando de una solución inicial

	* **terminationCondition:** Método que revisa si la condición de termino (temperatura mínima, número de evaluaciones o tiempo de ejecución) se ha cumplido

	* **getAcceptanceProbability:** Método que calcula la probabilidad de aceptar una solución

	* **reduceTemperature:** Método que reduce el valor de la temperatura siguiendo un esquema de enfriamiento seleccionado

* **GeneticAlgorithm.py:** Modulo con la clase que implementa el método de búsqueda de Algoritmo Genético

	* **search:** Método que inicia la búsqueda comenzando de una población inicial generada aleatoriamente

	* **terminationCondition:** Método que revisa si la condición de termino (número de evaluaciones, iteraciones o tiempo de ejecución) se ha cumplido

* **Population.py:** Modulo con la clase que implementa todos los métodos para manipular las soluciones de la población de algoritmo genético

	* **mutation:** Método que aplica un operador de mutación a la población

	* **crossover:** Método que aplica un operador de crossover a los padres proporcionados

	* **selectParents:** Método que selecciona dos padres aplicando un operador de selección

	* **selectPopulation:** Método que selecciona la población reduciendo su tamaño en base a un operador de selección
	
* **LocalSearch.py:** Modulo con la clase que implementa el método de búsqueda local

	* **search:** Método que aplica la búsqueda comenzando por una solución inicial

	* **swapSearch:** Método que aplica la búsqueda local mediante movimientos swap

	* **twoOptSearch:** Método que aplica la búsqueda local mediante 2-opt

	* **threeOptSearch:** Método que aplica la búsqueda local mediante 3-opt

	
* **IteratedLocalSearch.py:** Modulo con la clase que implementa el método de búsqueda local iterativo

	* **search:** Método que aplica la búsqueda comenzando por una solución inicial

	* **terminationCondition:** Método que revisa si la condición de termino (número de iteraciones o tiempo de ejecución) se ha cumplido
  

## Argumentos

Las opciones de los algoritmos se pueden cambiar en la clase AlgorithmsOptions.py, sin embargo, al crear la clase se le pueden entregar definiciones de las variables a definir, como por ejemplo: "options = AlgorithmsOptions(seed=98849,...)". O bien, si se es ejecutado directamente desde la línea de comando se le pueden pasar los siguientes argumentos:

Argumentos Generales:
  
* **Metaheurística:** Tipo de Metaheurística a usar. Por defecto SA
	* **SA:** Simulated Annealing 
	* **GA:** Genetic Algorithm.
	*  (-mh o --metaheuristic). **Ejemplo:** python tspf.py -mh SA

* **Instancia:** Ruta al archivo de la instancia de TSP a resolver. Por defecto instances/burma14.tsp.
	*  (-i o --instance **<PATH>**). **Ejemplo:** python tspf.py -i instances/eil51.tsp
  
* **Semilla**: Semilla para el generador de números aleatorios y todo los relacionado al módulo random de Python.
	*  (-s o --seed **entero**). **Ejemplo:** python tspf.py -s 4854

* **Movimiento:** Tipo de movimiento en formato TSPMove que se utilizara para la ejecución. Los valores posibles son TSPMove.SWAP, TSPMove.TWO_OPT y TSPMove.THREE_OPT. Por defecto se utiliza swap. 
	* (-mhm o --move **[ swap | 2opt | 3opt ]**). **Ejemplo:** python tspf.py --move 2opt
	
* **Evaluaciones:** Número máximo de funciones de evaluación calculadas. Por defecto se utiliza 1000
	 * (-e o --evaluations **entero**). **Ejemplo:** python tspf.py -e 2000

* **Iteraciones:** Número máximo de iteraciones para el ciclo principal de un algoritmo. Por defecto se utiliza 20
	 * (-e o --evaluations **entero**). **Ejemplo:** python tspf.py -it 500
	 
* **Archivo de solución y trayectoria:** Nombre del archivo de salida para almacenar la solución y la trayectoria. Por defecto se utiliza solution.txt y trajectory.csv
	 * (-sol o --solution <PATH>). **Ejemplo:** python tspf.py --solution test
	 
* **Visualización de trayectoria:** Parámetro de tipo flag que indica si se quiere o no visualizar la trayectoria de la solución.
	 * (-vi o --visualize). **Ejemplo:** python tspf.py --visualize

* **Modo Interfaz Grafica:** Parámetro de tipo flag que indica si se quiere o no utilizar el modo interfaz grafica.
	 * (-gui o --gui). **Ejemplo:** python tspf.py --gui

Argumentos para Simulated Annealing:

* **Solución Inicial:** Tipo de solución inicial en formato InitialSolution que se utilizara. Los valores posibles son: InitialSolution.RANDOM, InitialSolution.NEAREST_N y InitialSolution.DETERMINISTIC. Por defecto se utiliza random. 
	* (-is o --insol **[ random | nearest_n | deterministic ]**). **Ejemplo:** python tspf.py --insol deterministic

* **Enfriamiento:** Variable del tipo CoolingType que indica el tipo de esquema de enfriamiento que se utilizara para la ejecución de Simulated Annealing. Los valores posibles son: CoolingType.GEOMETRIC, CoolingType.LOG y CoolingType.LINEAR. Por defecto se utiliza geometric.

	* (-c o --cooling **[ linear | geometric | log ]**). **Ejemplo:** python tspf.py -c linear

* **Alfa:** Valor del parámetro Alpha para el enfriamiento lineal. Por defecto 0.98.

	* (-a o --alpha **]0,1]**). **Ejemplo:** python tspf.py -a 0.3
  

* **Temperatura Inicial:** Valor de la temperatura inicial t0. Por defecto 1000.0. 
	* (-t0 o --tini **]0,FLOAT_MAX]**). **Ejemplo:** python tspf.py -t0 956.45

* **Temperatura Mínima:** Valor de la temperatura mínima. Por defecto 900.0.
	*  (-tmin o --tmin **]0,FLOAT_MAX]**). **Ejemplo:** python tspf.py -tmin 800.87

Argumentos para Algoritmo Genético:

* **Tamaño de la población:** Tamaño de la población. Por defecto 10

	* (-p o --psize **]0,INT_MAX]**). **Ejemplo:** python tspf.py -p 20

* **Cantidad de hijos:** Cantidad de hijos a generar. Por defecto 20

	* (-o o --osize **]0,INT_MAX]**). **Ejemplo:** python tspf.py -o 40

* **Selección de padres:** Los valores posibles son: SelectionType.BEST, SelectionType.RANDOM, SelectionType.ROULETTE y SelectionType.TOURNAMENT. Por defecto random

	* (-ps o --pselection **[ random | best | roulette | tournament ]**). **Ejemplo:** python tspf.py --pselection tournament

* **Operador de cruzamiento:** Los valores posibles son: CrossoverType.OX, CrossoverType.PMX y CrossoverType.OPX. Por defecto ox

	* (-cr o --crossover **[ ox | opx | pmx ]**). **Ejemplo:** python tspf.py --crossover opx

* **Operador de mutación:** Los valores posibles son: TSPMove.SWAP, TSPMove.TWO_OPT y TSPMove.THREE_OPT. Por defecto swap 

	* (-mu o --mutation **[ swap | 2opt | 3opt ]**). **Ejemplo:** python tspf.py -mu 2opt

* **Probabilidad de mutación:** Valor de probabilidad de mutación de los individuos. Por defecto 0.2.

	* (-mp o --mprobability **[0,1]**). **Ejemplo:** python tspf.py -mp 0.3
  
* **Selección de poblacion: ** Los valores posibles son: SelectionType.BEST, SelectionType.RANDOM, SelectionType.ROULETTE y SelectionType.TOURNAMENT. Por defecto random

	* (-gs o --gselection **[ random | best | roulette | tournament ]**). **Ejemplo:** python tspf.py --gselection tournament

* **Estrategia de selección de población:** Los valores posibles son: SelectionStrategy.MULAMBDA y SelectionStrategy.MUPLUSLAMBDA. Por defecto mu,lambda

	* (-g o --gstrategy **[ mu,lambda | mu+lambda ]**). **Ejemplo:** python tspf.py --gstrategy mu,lambda

Argumentos para Local Search e Iterated Local Search:

* **Movimiento:** Tipo de movimiento en formato TSPMove que se utilizara para la ejecución. Los valores posibles son TSPMove.SWAP, TSPMove.TWO_OPT y TSPMove.THREE_OPT. Por defecto se utiliza swap. 
	* (-mhm o --move **[ swap | 2opt | 3opt ]**). **Ejemplo:** python tspf.py --move 2opt

* **Best Improvemet:** Parámetro de tipo flag que indica si la búsqueda es del tipo best improvement o first improvement, se deja por defecto first improvement.
	 * (-b o --best). **Ejemplo:** python tspf.py --best
	 
* **Perturbación:** Tipo de movimiento en formato PerturbationType que se utilizara para la perturbacion. Los valores posibles son PerturbationType.SWAP, PerturbationType.TWO_OPT, PerturbationType.THREE_OPT y PerturbationType.RANDOM. Por defecto se utiliza swap. 
	* (-per o --perturbation **[ swap | 2opt | 3opt | random ]**). **Ejemplo:** python tspf.py --move 2opt
	 
* **Número de Perturbaciones:** Número máximo de perturbaciones por iteración en Itarated Local Search. Por defecto se utiliza 3
	 * (-np o --nperturbations **entero**). **Ejemplo:** python tspf.py -np 5
