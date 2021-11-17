"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT.graph import gr
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
assert cf


def new_analyzer():
    """
    Inicializa el analizador
    digraph: Dígrafo en el cual se incluirán la totalidad de los
             aeropuertos (airports_full.csv) y las rutas dirigidas
             especificadas en el archivo full_routes.csv
    graph: Grafo no dirigido en el cual se incluirán solamente los
           aeropuertos y las rutas que tengan tanto una ruta de ida
           entre los dos aeropuertos como una de vuelta.
    airports: Tabla de hash que tiene como llaves las abreviaturas AITA
              de cada aeropuerto que es un vértice del dígrafo 
              'digraph' y como valores arreglos con todos los otros
              aeropuertos a los que se puede llegar desde ahí.


    components: Almacena la información de los componentes conectados.
    paths: Estructura que almancena los caminos de costo mínimo desde un
           vértice determinado a todos los otros vértices del grafo
    """
    try:
        analyzer = {
                    'digraph': None,
                    'graph': None,
                    'airports': None,
                    'components': None,  # TODO: ¿Necesario?
                    'paths': None  # TODO: ¿Necesario?
                    }


        analyzer['digraph'] = gr.newGraph(datastructure='ADJ_LIST',
                                                 directed=True,
                                                 size=10700,
                                                 comparefunction=compare)
        analyzer['graph'] = gr.newGraph(datastructure='ADJ_LIST',
                                        directed=False,
                                        size=10700,  # TODO: cambiar el tamaño
                                        comparefunction=compare)
        analyzer['airports'] = mp.newMap(numelements=10700,
                                         maptype='PROBING',
                                         comparefunction=compare)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model: new_analyzer')


# Functions that add information to the analyzer


def add_airport(analyzer, airport):
    """
    Añade la abreviación AITA de cada aeropuerto en el archivo 
    airports_full.csv como un vértice de el dígrafo 'digraph' del
    Analizador.
    """
    try:
        if not gr.containsVertex(analyzer['digraph'], airport['IATA']):
            gr.insertVertex(analyzer['digraph'], airport['IATA'])
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model: add_airport')


def add_route_digraph(analyzer, route):
    """
    Añade un arco dirigido al dígrafo 'digraph' del Analizador.
    """
    try:
        origin = route['Departure']
        destination = route['Destination']
        distance = float(route['distance_km'])
        edge = gr.getEdge(analyzer['digraph'], origin, destination)
        if edge is None:
            gr.addEdge(analyzer['digraph'], origin, destination, distance)
    except Exception as exp:
        error.reraise(exp, 'model: add_route_digraph: add_edge')

    try:
        airport_exists = mp.contains(analyzer['airports'], origin)
        if airport_exists:
            airport_entry = mp.get(analyzer['airports'], origin)
            array = me.getValue(airport_entry)
            lt.addLast(array, destination)
        else:
            array = lt.newList(datastructure='ARRAY_LIST')
            lt.addLast(array, destination)
            mp.put(analyzer['airports'], origin, array)
    except Exception as exp:
        error.reraise(exp, 'model: add_route_digraph: put_hashtable')
    

def add_route_graph(analyzer, route):
    """
    Añade un arco al grafo 'graph' del Analizador.
    """
    try:
        origin = route['Departure']
        destination = route['Destination']
        distance = float(route['distance_km'])
        edge = gr.getEdge(analyzer['graph'], origin, destination)
        """
        Given that the graph is not directed, when invoking 
        gr.addEdge(graph, origin, destination) not only an edge
        origin -> destination is added but also an edge
        destination -> origin. Due to that, when using 'origin' and
        'destination' as parameters of gr.getEdge() or gr.addEdge()
        their positions are interchangeable.
        """
        if edge is None:
            gr.addEdge(analyzer['graph'], origin, destination, distance)

        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model: add_route_graph')


# Construccion de modelos

# Funciones para agregar informacion al analizador

# Funciones para creacion de datos

# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento

# Requirements


def requirement1():
    pass


def requirement2():
    pass


def requirement3():
    pass


def requirement4():
    pass


def requirement5():
    pass


def requirement6():
    pass


# Comparison functions


def compare(thing1, thing2):
    """
    Generic comparison function.
    """
    if thing1 == thing2:
        return 0
    elif thing1 > thing2:
        return 1
    else:
        return -1


def compareStopIds(stop, keyvaluestop):
    """
    Compara dos estaciones
    """
    stopcode = keyvaluestop['key']
    return compare(stop, stopcode)