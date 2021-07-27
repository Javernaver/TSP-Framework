

seed : int


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def swap2 (v, v2, i, j):
    # Funcion: rutina auxiliar para ordenar un arreglo de enteros
    # Input: dos arreglos, dos indices
    # Output: dos arreglos ordenados
    # Comentarios: los elementos en la posicion i y j de las dos matrices
    #              se intercambian

    aux = int
    aux = v[i]
    v[i] = v[j]
    v[j] = aux
    aux = v2[i]
    v2[i] = v2[j]
    v2[j] = aux

def sort2 (v, v2, left, right):
    # Funcion: rutina recursiva (quicksort) para ordenar un arreglo.
    #          El segundo arreglo hace la misma secuencia de intercambio
    # Input: dos arreglos, dos indices
    # Output: ordenamiento de dos arreglos
    # Comentarios: los elementos en la posicion i y j de las dos matrices
    #              se intercambian

    k = int
    last = int

    if (left >= right):
        return
    swap2(v, v2, left, int((left + right) / 2))
    last = left
    k = left + 1
    for k in range(right + 1):
        if(v[k] < v[left]):
            #last = last + 1
            swap2(v, v2, ++last, k)
    swap2(v, v2, left, last)
    sort2(v, v2, left, last)
    sort2(v, v2, last + 1, right)

def dtrunc (x):
    #Funcion: truncar un numero float
    #Output: numero float sin parte decimal

    k = int(x)
    x = float(k)
    return x
