import heapq
import math
import argparse
import time
import os
import copy

def getDistance(minNode, neighbor, distances):
    """
    Obtiene la distancia de la arista (currentNode, neighbor)
    :param currentNode: nodo inicial de la arista.
    :param neighbor: nodo final de la arista.
    :param distances: dict (nodoInicial, nodoFinal):distancia
    :return dist: distancia de la arista (currentNode, neighbor) 
    """
    queryList = str((minNode, neighbor))
    dist = distances[queryList]
    return dist

def buildGraphRepr():
    """
    Construye las representaciones para procesar el grafo, utilizando una lista de adyacencia 
    y una estructura de datos para almacenar las distancias.

    :return:
        -adjList: lista de adyacencia del grafo, dict node:listaNodosVecinos.
        -distances: dict (nodoInicial, nodoFinal):distancia
    """
    nNodes = int(open("nodos.txt", "r").read())
    enumNodes = list(range(1, nNodes + 1))

    adjList = {num:[] for num in enumNodes} 
    distances = {}

    #hay un archivo de arcos que es .dat
    try:
        edgeInfo = open("arcos.txt", "r")
    except:
        edgeInfo = open("arcos.dat", "r")
    for line in edgeInfo.readlines()[:-1]:
        entries = line.split()
        initNode = int(entries[0])
        finalNode = int(entries[1])
        distance = int(entries[2])
        adjList[initNode].append(finalNode)
        distances[str((initNode, finalNode))] = distance
    
    return adjList, distances

def dijkstra(initNode):
    """
    Implementacion de Dijkstra's algorithm. Utiliza un heap para obtener tiempo de ejecucion 
    mas rapido. La implementacion se realizo segun el material entregado.

    :param initNode: nodo inicial del algoritmo.
    :return:
        -preds: dict nodo:predecesor.
        -distanceLabel: dict nodo:distanciaPermanente.
    """

    #construye la representacion del grafo
    adjList, distances = buildGraphRepr()

    #comprobar que el nodo requerido existe, si no, error fatal
    if initNode > len(adjList.keys()):
        raise Exception('El nodo no se encuentra en el grafo')

    #comienza el cronometro
    start = time.time()

    #establece distancias infinitas a otros nodos
    distanceLabel = {num: math.inf for num in adjList if num != initNode}
    #establece distancia de nodo inicial
    distanceLabel[initNode] = 0

    #crea diccionario para nodos predecesores
    preds = {}
    #predecesor al inicio es el mismo inicial
    preds[initNode] = initNode

    iniHeap = []
    #crea heap...
    heapq.heapify(iniHeap)
    #...con las distancias temporales conocidas
    heapq.heappush(iniHeap, [distanceLabel[initNode], initNode])
    
    #mientras hayan elementos en el heap
    while len(iniHeap) != 0:
        minData = heapq.heappop(iniHeap)
        #se obtiene el nodo cuya distancia temporal es la minima
        minNode = minData[1]
        minNodeDist = minData[0]
        
        #por cada vecino del nodo...
        for neighbor in adjList[minNode]:
            #calcular la nueva distancia...
            value = distanceLabel[minNode] + getDistance(minNode, neighbor, distances)  
            #comprobar si la distancia se debe actualizar...
            if distanceLabel[neighbor] > value:
                #si el vecino no ha sido etiquetado...
                if distanceLabel[neighbor] == math.inf or value < distanceLabel[neighbor]:
                    distanceLabel[neighbor] = value
                    preds[neighbor] = minNode
                    #se inserta el vecino con la distancia temporal en el heap
                    heapq.heappush(iniHeap, [value, neighbor])
                else:
                    distanceLabel[neighbor] = value
                    preds[neighbor] = minNode
                    #se actualiza el nodo minimo con la distancia temporal nueva
                    if value < distanceLabel[minNode]:
                        heapq.heappush(iniHeap, [value, minNode])
    
    #termina el cronometro
    end = time.time()
    print("Nodos: " + str(len(adjList.keys())))
    print("Nodo inicial: " + str(initNode))
    print("Tiempo (s): " + str((end-start)))
    print("-----------------------------------------------------")

    #reemplaza distancias inf por -1 y establece predecesores en 0
    for key, value in list(distanceLabel.items()):
        if value == math.inf:
            distanceLabel[key] = -1
            preds[key] = 0
    
    return preds, distanceLabel

def dijkstra2(initNode):
    #construye la representacion del grafo
    adjList, distances = buildGraphRepr()
    numNodes = max(adjList.keys())
    
    #comprobar que el nodo requerido existe, si no, error fatal
    if initNode > len(adjList.keys()):
        raise Exception('El nodo no se encuentra en el grafo')

    #comienza el cronometro
    start = time.time()

    #establece distancias infinitas a otros nodos
    distanceLabel = {num: math.inf for num in adjList if num != initNode}
    #establece distancia de nodo inicial
    distanceLabel[initNode] = 0

    #crea diccionario para nodos predecesores
    preds = {}
    #predecesor al inicio es el mismo inicial
    preds[initNode] = initNode

    visited = set()
    toVisit = copy.deepcopy(distanceLabel)

    while len(visited) < numNodes:
        currentNode = min(toVisit, key = toVisit.get)
        visited.add(currentNode)
        del toVisit[currentNode]
        
        for neighbor in adjList[currentNode]:
            if distanceLabel[neighbor] > distanceLabel[currentNode] + getDistance(currentNode, neighbor, distances):
                distanceLabel[neighbor] = distanceLabel[currentNode] + getDistance(currentNode, neighbor, distances)
                toVisit[neighbor] = distanceLabel[currentNode] + getDistance(currentNode, neighbor, distances)
                preds[neighbor] = currentNode    

    #termina el cronometro
    end = time.time()
    print("Nodos: " + str(len(adjList.keys())))
    print("Nodo inicial: " + str(initNode))
    print("Tiempo (s): " + str((end-start)))
    print("-----------------------------------------------------")

    #reemplaza distancias inf por -1 y establece predecesores en 0
    for key, value in list(distanceLabel.items()):
        if value == math.inf:
            distanceLabel[key] = -1
            preds[key] = 0
    
    return preds, distanceLabel

def writeResults(initNode, preds, distanceLabel):
    """
    Escribe un archivo de salida según el formato solicitado.
    Primer registro consta del nodo fuente, cada registro siguiente consta de un nodo del 
    grafo, su correspondiente predecesor, y la etiqueta de distancia permanente asignada.

    :param initNode: nodo inicial del algoritmo.
    :param preds: dict nodo:predecesor.
    :param distanceLabel: dict nodo:distanciaFinal.
    """
    results = open("salidaDijkstra.txt", "w")
    results.write(str(initNode) + "\n")
    for key in sorted(list(distanceLabel.keys())):
        results.write(str(key) + " " + str(preds[key]) + " " + str(distanceLabel[key]) + "\n")
    return

def main():
    #parsear argumentos por linea de comando...
    parser = argparse.ArgumentParser()
    parser.add_argument('initNode', type=int, help='Se requiere un numero natural como nodo inicial')
    args = parser.parse_args()
    initNode = args.initNode
    #comprueba valores de nodo inicial
    if initNode <= 0:
        parser.error('Nodo inicial debe ser un numero natural')
    
    #cambio de directorio a instancias
    os.chdir("./instancias/")
    dirInstancias = next(os.walk('.'))[1]
    for dirIns in dirInstancias:
        os.chdir("./" + dirIns)
        #aplica dijkstra
        print("Algoritmo de Dijkstra")
        preds, distanceLabel = dijkstra(initNode)
        #escribe resultados
        writeResults(initNode, preds, distanceLabel)
        #subir un nivel de directorios
        os.chdir("..")

if __name__ == "__main__":
    main()