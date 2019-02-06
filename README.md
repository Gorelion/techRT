# Algoritmo de Dijkstra y Algoritmo de Dial

Este repositorio contiene las implementaciones del algoritmo de Dijkstra y algoritmo de Dial en Python 3.6.

La implementación del algoritmo de Dijkstra considera el uso de un min-heap, mientras que Dial considera una estructura de datos que simula una lista circular. Ambos algoritmos se implementaron según lo presentado por (Ahuja et al., 1988).

Cada algoritmo está implementado en su propio script, y se aplica a cada grafo del directorio "instancias", usando como nodo inicial aquel ingresado por consola.

# Uso

Se debe ejecutar cada script, indicando como argumento el número del nodo inicial.

```
python dial.py nodoInicial
```

```
python dijkstra.py nodoInicial
```

Para cada algoritmo, se muestra por consola su tiempo de ejecución, en segundos, para las instancias (grafos) entregadas, además del número de nodos totales del grafo procesado, y el nodo inicial del algoritmo.

Se debe notar que el tiempo de ejecución fue cronometrado considerando solo la ejecución de los algoritmos, y no, por ejemplo, el tiempo transcurrido en la construcción de las representaciones de los grafos.

En cada carpeta del directorio "./instancias", se genera un archivo "salidaDial.txt" con el formato requerido aplicando el algoritmo de Dial, y "salidaDijkstra.txt" en el caso del algoritmo de Dijkstra.

## Notas adicionales

El script dijkstra.py contiene un método llamado "dijkstra2". Se puede aplicar el algoritmo de Dijkstra ocupando este método, solo que se debe cambiar directamente en el código. Esta es la implementación estándar de Dijkstra, y no la recomiendo usar, pues es considerablemente más lenta que la principal utilizada (de hecho, en mi computador ni termina con los grafos más grandes).

Tal como se indica en la teoría, el algoritmo de Dial es consistentemente más rápido que el algoritmo de Dijkstra.

Alguna puntuación en la documentación del código fue omitida para evitar problemas de compatibilidad.

# Referencias

    Ahuja, R. K., Magnanti, T. L., & Orlin, J. B. (1988). Network flows.