import heapq
import math
import argparse
import time
import os

def onlyEmptyBuckets(buckets):
    """
    Comprueba si todos los buckets estan vacios.

    :param buckets: dict distancia:nodosConEsaDistancia.
    :return: True si solo hay buckets vacios, False de otro modo.
    """
    for _, value in buckets.items():
        if len(value) > 0:
            return False
    return True

def getDistance(currentNode, neighbor, distances):
    """
    Obtiene la distancia de la arista (currentNode, neighbor)
    :param currentNode: nodo inicial de la arista.
    :param neighbor: nodo final de la arista.
    :param distances: dict (nodoInicial, nodoFinal):distancia
    :return dist: distancia de la arista (currentNode, neighbor) 
    """
    queryList = str((currentNode, neighbor))
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

def dial(initNode):
    """
    Implementacion de Dial's algorithm. Utiliza aritmetica modular para simular una lista 
    circular de buckets. La implementacion se realizo segun el material entregado.

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

    #obtiene la arista mas pesada del grafo
    maxEdge = max(distances.values())
    
    #estructura de datos para buckets, simula una lista circular. contiene maxEdge + 1 buckets.
    buckets = {k:[] for k in range(maxEdge + 1)}
    #establece distancias infinitas a otros nodos
    distanceLabel = {num: math.inf for num in adjList if num != initNode}
    #establece distancia de nodo inicial
    distanceLabel[initNode] = 0
    
    #crea diccionario para nodos predecesores
    preds = {}
    #predecesor al inicio es el mismo inicial
    preds[initNode] = initNode
    #al comienzo el unico nodo con distancia es el inicial
    buckets[0].append(initNode)

    #comienza el cronometro
    start = time.time()

    idx = 0
    #se considera como algoritmo de punto fijo
    while(True):
        #si no hay nodos ocupados, el algoritmo termina
        if onlyEmptyBuckets(buckets):
            break
        
        #evita overflow y simula comportamiento de lista circular
        if idx == maxEdge + 1:
            idx = idx % (maxEdge + 1)
        
        #si el bucket idx esta vacio, se salta al siguiente
        if len(buckets[idx]) == 0:
            idx += 1
            continue
        
        #nodos del primer bucket no vacio
        bucketNodes = buckets[idx]
        
        #por cada nodo en el bucket...
        for bNode in bucketNodes:
            #por cada vecino del nodo...
            for neighbor in adjList[bNode]:
                #obtiene distancia de la arista...
                dist = getDistance(bNode, neighbor, distances)
                #comprueba si se debe actualizar la distancia...
                if distanceLabel[neighbor] > distanceLabel[bNode] + dist:
                    #actualiza distancia
                    distanceLabel[neighbor] = distanceLabel[bNode] + dist
                    #asigna predecesor
                    preds[neighbor] = bNode
                    #calcula en que bucket deberia ir el nodo cuya distancia se actualizo
                    newIdx = (distanceLabel[bNode] + dist) % (maxEdge + 1)
                    #se cambia de bucket al nodo actualizado
                    buckets[newIdx].append(neighbor)

        #se vacia el bucket
        buckets[idx] = []
    
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
    results = open("salidaDial.txt", "w")
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
        #aplica Dial
        print("Algoritmo de Dial")
        preds, distanceLabel = dial(initNode)
        #escribe resultados
        writeResults(initNode, preds, distanceLabel)
        #subir un nivel de directorios
        os.chdir("..")

if __name__ == "__main__":
    main()