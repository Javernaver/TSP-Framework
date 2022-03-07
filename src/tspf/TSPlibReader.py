"""
Modulo con clases y metodos para la lectura, calculo y generacion de matrices con las distancias con los archivos
que contengan porblemas TSP en formato TSPlib 

"""

from . import os, sys, Enum, math, Decimal
from .Tools import utilities, bcolors

class Point():
    """ Clase puntero para coordenadas """
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

class Distance():
    """ Clase de apoyo para ayudar a crear la matriz del vecindario para los nodos """
    def __init__(self, val, pos) -> None:
        self.distance = val
        self.position = pos

class Distance_type(Enum):
    """Tipos de instancias en TSPlib"""
    EUC_2D = 'EUC_2D'
    CEIL_2D = 'CEIL_2D'
    GEO = 'GEO'
    ATT = 'ATT'


class TSPlibReader():

    # Arreglo de estructuras que contiene las coordenadas, Tipo Point
    nodeptr = []
    # Variable que indica el tipo de distancia
    distance_type: Distance_type
    # Matriz de distancia: distancia de nodos i a j
    distance = []
    # Lista de vecinos mas cercanos: para cada nodo i una lista de vecinos ordenados
    nn_list = []
    # Numero de nodos
    n = 0
    # Nombre del archivo de instancia
    name = ''
    # modo Gui
    gui = False
    # error
    error = ''

    def __init__(self, tsp_file_name: str):
        """ Constructor clase TSPlibReader recibe la ruta al archivo de la instancia"""

        try:
            # Leer instancia desde un archivo
            self.nodeptr = self.read_etsp(tsp_file_name)
           
        except:
            if not self.gui:
                print(f"{bcolors.FAIL}Error: No se pudo leer el archivo.{bcolors.ENDC}")
                exit()
        if not self.error:
            # Obtener la matriz de distancias
            print('Calculando las distancias...')
            self.compute_distances()
            # Generar listas de vecinos ordenados
            print('Calculando los vecinos...')
            self.compute_nn_lists()
            print(f"instancia {self.name} tiene {self.n} nodos")
            #print(self.distance)
            #print(self.nn_list)


    def read_etsp(self, tsp_file_name: str) -> list:
        """ Lectura y parsing de instancia TSPlib (archivo de instancia debe estar en formato TSPLIB)

            Parameters
            ----------
            tsp_file_name : str
                ruta al archivo de instancia
            
            Returns
            -------
            list
                lista de coordenas
        """
        buf = ''
       
        nodeptr = []

        i = 0

        # Encontrado seccion de coordenadas
        found_coord_section = False

        if (tsp_file_name == None):
            if not self.gui:
                print(f"{bcolors.FAIL}Error: Instancia no especificada, abortando...{bcolors.ENDC}")
                exit()
            else:
                self.error = 'Instancia no especificada'
                return

        if(not(os.access(tsp_file_name, os.R_OK))):
            if not self.gui:
                print(f"{bcolors.FAIL}Error: No se puede leer el archivo {tsp_file_name}{bcolors.ENDC}")
                print(f"{bcolors.BOLD}Si esta utilizando el framework desde otra carpeta recuerde agregar la instancia tsp con el parametro (-i <PATH> o --instance <PATH>) {bcolors.ENDC}")  
            
                exit()
            else:
                self.error = 'No se puede leer el archivo'
                return
            
        print(f"Leyendo archivo TSPlib {tsp_file_name} ... ")
        archivo = open(tsp_file_name, "r")
        linea = archivo.readline()
        while linea:
            if(linea.find("EOF") != -1):
                break
            if(found_coord_section == False):
                if(linea.startswith("NAME")):
                    self.name = linea[linea.find(":")+2:len(linea)-1]

                elif(linea.startswith("TYPE") and linea.find("TSP") == -1):
                    if not self.gui:
                        print(f"{bcolors.FAIL}Instancia no esta en el formato TSPLIB !!{bcolors.ENDC}")
                        exit()
                    else:
                        self.error += 'Instancia no esta en el formato TSPLIB !!'
                        return
                elif(linea.startswith("DIMENSION")):
                    self.n = int(linea[linea.find(":")+2 : len(linea)-1])
                    nodeptr = [Point] * self.n
                else:
                    if(linea.startswith("EDGE_WEIGHT_TYPE")):
                        buf = linea[linea.find(":")+2 : len(linea)-1]
                        if(buf == "EUC_2D"):
                            self.distance_type = Distance_type.EUC_2D
                        elif(buf == "CEIL_2D"):
                            self.distance_type = Distance_type.CEIL_2D
                        elif(buf == "GEO"):
                            self.distance_type = Distance_type.GEO
                        elif(buf == "ATT"):
                            self.distance_type = Distance_type.ATT
                        else:
                            if not self.gui:
                                print(f"{bcolors.FAIL}EDGE_WEIGHT_TYPE {buf} no implementado en la clase.{bcolors.ENDC}")
                                exit()
                            else:
                                self.error = f'EDGE_WEIGHT_TYPE {buf} no implementado en la clase.'
                                return
            else:
                  
                city_info = linea.split()
                nodeptr[i] = Point(float(city_info[1]), float(city_info[2]))
                i += 1
                
            
            if (linea.startswith("NODE_COORD_SECTION")):
                found_coord_section = True

            linea = archivo.readline()
    
        if (found_coord_section == False):
            if not self.gui:
                print("Error: Ocurrio al buscar el inicio de las coordenadas !!")
                exit()
            else:
                self.error = 'Ocurrio al buscar el inicio de las coordenadas !!'
                return

        archivo.close()
        
        return nodeptr

    def round_distance(self, i, j) -> int:
        """ Computa la distancia Euclidiana (redondea al siguiente entero) entre dos nodos.
            Para una definicion de como calcular esta distancia vea TSPLIB en caso de ser 1.5 -> 2 y 2.5 -> 2

            Parameters
            ----------
            i, j : int | float
                coordenadas
            
            Returns
            -------
            int
                distancia entre dos nodos
        """      
        diferencia_x = self.nodeptr[i].x - self.nodeptr[j].x
        diferencia_y = self.nodeptr[i].y - self.nodeptr[j].y
        distancia = math.sqrt(pow(diferencia_x,2) + pow(diferencia_y,2)) 
        return round(distancia)

    def ceil_distance (self, i, j) -> int:
        """ Computa la distancia Euclidiana (usando funcion techo) entre dos nodos.
            Para una definicion de como calcular esta distancia vea TSPLIB
            la funcion math, redondea al entero mayor en caso de ser 1.1 -> 2 y 1.9 -> 2

            Parameters
            ----------
            i, j : int | float
                coordenadas
            
            Returns
            -------
            int
                distancia entre dos nodos
        """
        diferencia_x = self.nodeptr[i].x - self.nodeptr[j].x
        diferencia_y = self.nodeptr[i].y - self.nodeptr[j].y
        distancia = round(math.sqrt(pow(diferencia_x,2) + pow(diferencia_y,2)),2)
        return math.ceil(distancia)

    def geo_distance(self, i, j) -> int:
        """ Computa la distancia geografica (redondeada al siguiente entero) entre dos nodos
            Adaptada desde el codigo de concorde. Para una definicion de como calcular esta distancia vea TSPLIB

            Parameters
            ----------
            i, j : int | float
                coordenadas
            
            Returns
            -------
            int
                distancia entre dos nodos
        """
        deg = float
        min = float
        lati = float
        latj = float
        longi = float
        longj = float
        q1 = float
        q2 = float
        q3 = float
        dd = int
        x1 = self.nodeptr[i].x
        x2 = self.nodeptr[j].x
        y1 = self.nodeptr[i].y
        y2 = self.nodeptr[j].y
        RRR = 6378.388

        deg = utilities.dtrunc(x1)
        min = float(Decimal(f"{x1}") - Decimal(f"{deg}"))
        lati = math.pi * (deg + 5.0 * min / 3.0) / 180.0
        deg = utilities.dtrunc(x2)
        min = float(Decimal(f"{x2}") - Decimal(f"{deg}"))
        latj = math.pi * (deg + 5.0 * min / 3.0) / 180.0

        deg = utilities.dtrunc(y1)
        min = float(Decimal(f"{y1}") - Decimal(f"{deg}"))
        longi = math.pi * (deg + 5.0 * min / 3.0) / 180.0
        deg = utilities.dtrunc(y2)
        min = float(Decimal(f"{y2}") - Decimal(f"{deg}"))
        longj = math.pi * (deg + 5.0 * min / 3.0) / 180.0

        q1 = math.cos(float(Decimal(f"{longi}") - Decimal(f"{longj}")))
        q2 = math.cos(float(Decimal(f"{lati}") - Decimal(f"{latj}")))
        q3 = math.cos(float(Decimal(f"{lati}") + Decimal(f"{latj}")))
        dd = int(RRR * math.acos(0.5 * ((1.0 + q1) * q2 - (1.0 - q1) * q3))+ 1.0)
        return dd

    def att_distance(self, i, j) -> int:
        """ Computa la distancia ATT (redondeada al siguiente entero) entre dos nodos
            Adaptada desde el codigo de concorde. Para una definicion de como calcular esta distancia vea TSPLIB

            Parameters
            ----------
            i, j : int | float
                coordenadas
            
            Returns
            -------
            int
                distancia entre dos nodos
        """
        diferencia_x = Decimal(f"{self.nodeptr[i].x}") - Decimal(f"{self.nodeptr[j].x}")
        diferencia_y = Decimal(f"{self.nodeptr[i].y}") - Decimal(f"{self.nodeptr[j].y}")
        rij = math.sqrt(float(pow(diferencia_x,2) + pow(diferencia_y,2)) / 10.0)
        tij = utilities.dtrunc(rij)

        if (tij < rij):
            dij = int(tij + 1)
        else:
            dij = int(tij)
        return dij

    def compute_distances(self):
        """ Computa y guarda las distancias entre los nodos generando una lista de listas (matriz)
            y la guarda en la variable distance """
            
        matrix = []
        
        for i in range(self.n):

            matrix.append([])

            for j in range(self.n):

                if (self.distance_type == Distance_type.EUC_2D):
                    matrix[i].append(self.round_distance(i,j))
                elif (self.distance_type == Distance_type.CEIL_2D):
                    matrix[i].append(self.ceil_distance(i,j))
                elif (self.distance_type == Distance_type.GEO):
                    matrix[i].append(self.geo_distance(i,j))
                elif (self.distance_type == Distance_type.ATT):
                    matrix[i].append(self.att_distance(i,j))

        self.distance = matrix     

    def compute_nn_lists(self):
        """ Computa y guarda la lista de vecinos mas cercanos a cada nodo y genera una lista de listas (matriz) 
            que se guarda en la variable nn_list """

        distance_value = 0 # valor de distancia
        distances = [Distance] * self.n # lista para las distancias del vecindario 
        nn = self.n - 1 
        m_nnear = [] # matriz del vecindario

        for node in range(self.n): # Recorrer los nodos

            for i in range(self.n): # Preparar distancias de la seccion
                
                distance_value = self.distance[node][i] # se guardan los valores de distancia
                distances[i] = Distance(distance_value, i) # 
                
            #print(distance_values, [distance.distance for distance in distances])
            distances[node].distance = sys.maxsize # Ciudad no es el vecino mas cercano y se le da un valor altisimo
            
            distances.sort(key=lambda dist: dist.distance) # ordenar de menor a mayor
            #print(distance_values, [distance.distance for distance in distances])

            # Crear seccion del vecindario con las posiciones de los vecinos
            m_nnear.append([])
            for i in range(nn): 
                m_nnear[node].append(distances[i].position)

        self.nn_list = m_nnear