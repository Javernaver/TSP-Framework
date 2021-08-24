from decimal import *
import os
import math
from src import Utilities
import sys
from enum import Enum

class Point:
    """ Clase puntero para coordenadas """
    def __init__(self, x, y):
        self.x = x
        self.y = y

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
    distance_type :Distance_type
    # Matriz de distancia: distancia de nodos i a j
    distance = [[]]
    # Lista de vecinos mas cercanos: para cada nodo i una lista de vecinos ordenados
    nn_list = [[]]
    # Numero de nodos
    n = 0
    # Nombre del archivo de instancia
    name = ''

    def __init__(self, tsp_file_name):
        # Funcion: Constructor clase TSPlibReader
        # Input: Ruta al archivo de la instancia

        try:
            # Leer instancia desde un archivo
            self.nodeptr = self.read_etsp(tsp_file_name)
        except:
            print("Error: No se tiene acceso al archivo.")
            exit()
        # Obtener la matriz de distancias
        self.compute_distances()
        print('computadas las distancias')
        # Generar listas de vecinos ordenados
        self.compute_nn_lists()
      
        print(f"# instancia {self.name} tiene {self.n} nodos")

    def read_etsp (self, tsp_file_name):
        # Funcion: lectura y parsing de instancia TSPlib
        # Input: ruta al archivo de instancia
        # Output: arreglo de coordenas
        # Comentario: archivo de instancia debe estar en formato TSPLIB
        buf = ''
        global distance_type 
        global nodeptr 

        i = 0

        # Encontrado seccion de coordenadas
        found_coord_section = False

        if (tsp_file_name == None):
            print("Error: Instancia no especificada, abortando...")
            exit()

        if(not(os.access(tsp_file_name, os.R_OK))):
            print(f"Error: No se puede leer el archivo {tsp_file_name}")
            exit()
            
        print(f"# Leyendo archivo TSPlib {tsp_file_name} ... ")
        archivo = open(tsp_file_name, "r")
        linea = archivo.readline()
        while linea:
            if(linea.find("EOF") != -1):
                break
            if(found_coord_section == False):
                if(linea.startswith("NAME")):
                    self.name = linea[linea.find(":")+2:len(linea)-1]

                elif(linea.startswith("TYPE") and linea.find("TSP") == -1):
                    print("Instancia no esta en el formato TSPLIB !!")
                    exit()
                elif(linea.startswith("DIMENSION")):
                    self.n = int(linea[linea.find(":")+2 : len(linea)-1])
                    nodeptr = [Point] * self.n
                else:
                    if(linea.startswith("EDGE_WEIGHT_TYPE")):
                        buf = linea[linea.find(":")+2 : len(linea)-1]
                        if(buf == "EUC_2D"):
                            distance_type = Distance_type.EUC_2D
                        elif(buf == "CEIL_2D"):
                            distance_type = Distance_type.CEIL_2D
                        elif(buf == "GEO"):
                            distance_type = Distance_type.GEO
                        elif(buf == "ATT"):
                            distance_type = Distance_type.ATT
                        else:
                            print(f"EDGE_WEIGHT_TYPE {buf} no implementado en la clase.")
                            exit()
            else:
                  
                city_info = linea.split()
                nodeptr[i] = Point(float(city_info[1]), float(city_info[2]))
                i += 1
                
            
            if (linea.startswith("NODE_COORD_SECTION")):
                found_coord_section = True

            linea = archivo.readline()
    
        if (found_coord_section == False):
            print("Error: Ocurrio al buscar el inicio de las coordenadas !!")
            exit()

        archivo.close()
        
        return nodeptr

    def round_distance (self, i, j):
        # Funcion: computa la distancia Euclidiana (redondea al siguiente entero) entre dos nodos
        # Input: indices de dos nodos
        # Output: distancia entre dos nodos
        # Comentarios: para una definicion de como calcular esta distancia vea TSPLIB
        #              la funcion round, rendondea al entero mas cercano
        #              en caso de ser 1.5 -> 2 y 2.5 -> 2
        
        diferencia_x = nodeptr[i].x - nodeptr[j].x
        diferencia_y = nodeptr[i].y - nodeptr[j].y
        distancia = math.sqrt(pow(diferencia_x,2) + pow(diferencia_y,2)) 
        return round(distancia)

    def ceil_distance (self, i, j):
        # Funcion: computa la distancia Euclidiana (usando funcion techo) entre dos nodos
        # Input: indices de dos nodos
        # Output: distancia entre dos nodos
        # Comentarios: para una definicion de como calcular esta distancia vea TSPLIB
        #              la funcion math, redondea al entero mayor
        #              en caso de ser 1.1 -> 2 y 1.9 -> 2

        diferencia_x = self.nodeptr[i].x - self.nodeptr[j].x
        diferencia_y = self.nodeptr[i].y - self.nodeptr[j].y
        distancia = round(math.sqrt(pow(diferencia_x,2) + pow(diferencia_y,2)),2)
        return math.ceil(distancia)

    def geo_distance (self, i, j):
        # Funcion: computa la distancia geografica (redondeada al siguiente entero)
        #          entre dos nodos
        # Input: indices de dos nodos
        # Output: distancia entre dos nodos
        # Comentarios: adaptada desde el codigo de concorde. Para una definicion de
        #              como calcular esta distancia vea TSPLIB

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
        x1 = nodeptr[i].x
        x2 = nodeptr[j].x
        y1 = nodeptr[i].y
        y2 = nodeptr[j].y
        RRR = 6378.388

        deg = Utilities.dtrunc(x1)
        min = float(Decimal(f"{x1}") - Decimal(f"{deg}"))
        lati = math.pi * (deg + 5.0 * min / 3.0) / 180.0
        deg = Utilities.dtrunc(x2)
        min = float(Decimal(f"{x2}") - Decimal(f"{deg}"))
        latj = math.pi * (deg + 5.0 * min / 3.0) / 180.0

        deg = Utilities.dtrunc(y1)
        min = float(Decimal(f"{y1}") - Decimal(f"{deg}"))
        longi = math.pi * (deg + 5.0 * min / 3.0) / 180.0
        deg = Utilities.dtrunc(y2)
        min = float(Decimal(f"{y2}") - Decimal(f"{deg}"))
        longj = math.pi * (deg + 5.0 * min / 3.0) / 180.0

        q1 = math.cos(float(Decimal(f"{longi}") - Decimal(f"{longj}")))
        q2 = math.cos(float(Decimal(f"{lati}") - Decimal(f"{latj}")))
        q3 = math.cos(float(Decimal(f"{lati}") + Decimal(f"{latj}")))
        dd = int(RRR * math.acos(0.5 * ((1.0 + q1) * q2 - (1.0 - q1) * q3))+ 1.0)
        return dd

    def att_distance (self, i, j):
        # Funcion: computa la distancia ATT (redondeada al siguiente entero) entre
        #          dos nodos
        # Input: indices de dos nodos
        # Output: distancia entre dos nodos
        # Comentarios: para un definicion de como calcular esta distancia vea TSPLIB

        diferencia_x = Decimal(f"{nodeptr[i].x}") - Decimal(f"{nodeptr[j].x}")
        diferencia_y = Decimal(f"{nodeptr[i].y}") - Decimal(f"{nodeptr[j].y}")
        rij = math.sqrt(float(pow(diferencia_x,2) + pow(diferencia_y,2)) / 10.0)
        tij = Utilities.dtrunc(rij)

        if (tij < rij):
            dij = int(tij + 1)
        else:
            dij = int(tij)
        return dij

    def compute_distances(self):
        """ computa y guarda las distancias entre los nodos en la variable disntance """
            
        matrix = [[]]
        
        for i in range(self.n):
            for j in range(self.n):
                if (distance_type == Distance_type.EUC_2D):
                    matrix.append([])
                    matrix[i].append(self.round_distance(i,j))
                elif (distance_type == Distance_type.CEIL_2D):
                    matrix.append([])
                    matrix[i].append(self.ceil_distance(i,j))
                elif (distance_type == Distance_type.GEO):
                    matrix.append([])
                    matrix[i].append(self.geo_distance(i,j))
                elif (distance_type == Distance_type.ATT):
                    matrix.append([])
                    matrix[i].append(self.att_distance(i,j))

        self.distance = matrix.copy()     

    def compute_nn_lists(self):
        """ computa y guarda la lista de vecinos mas cercanos a cada nodo en la variable nn_list """

        distance_vector = []
        help_vector = []
        m_nnear = [[]]

        nn = (self.n - 1)
        for node in range(self.n): # Computar cnd-sets para todos los nodos
            for i in range(self.n): # Copiar distancias desde nodo hacia otros nodos
                if (node == 0):
                    distance_vector.append(self.distance[node][i])
                    help_vector.append(i)
                else:
                    distance_vector[i] = self.distance[node][i]
                    help_vector[i] = i
            distance_vector[node] = sys.maxsize # Ciudad no es el vecino mas cercano
            Utilities.sort2(distance_vector, help_vector, 0, self.n-1)
            for i in range(nn):
                m_nnear.append([])
                m_nnear[node].append(help_vector[i])
        
        self.nn_list = m_nnear.copy()

