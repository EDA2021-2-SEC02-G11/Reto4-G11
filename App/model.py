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
    routes: Tabla de hash que tiene como llaves las abreviaturas AITA
            de cada aeropuerto y como valores arreglos con todos los 
            otros aeropuertos que son posibles destinos de ese.
    airports: Tabla de hash que tiene como llaves las abreviaturas AITA
              de cada aeropuerto y como valores el diccionario con la 
              información del aeropuerto.
    cities: Tabla de hash que tiene como llaves los nombres de las
            ciudades y como valores el diccionario con la información de
            la ciudad.
    components: Almacena la información de los componentes conectados.
    paths: Estructura que almancena los caminos de costo mínimo desde un
           vértice determinado a todos los otros vértices del grafo
    """
    try:
        analyzer = {
                    'digraph': None,
                    'graph': None,
                    'routes': None,
                    'airports': None,
                    'cities': None,
                    'components': None,  # TODO: Mirar si lo necesitaremos
                    'paths': None  # TODO: Mirar si lo necesitaremos
                    }


        analyzer['digraph'] = gr.newGraph(datastructure='ADJ_LIST',
                                          directed=True,
                                          size=10700,
                                          comparefunction=compare)
        analyzer['graph'] = gr.newGraph(datastructure='ADJ_LIST',
                                        directed=False,
                                        size=10700,  # TODO: mirar el tamaño
                                        comparefunction=compare)
        analyzer['routes'] = mp.newMap(numelements=10700,  # TODO: mirar tamaño
                                       maptype='PROBING',
                                       comparefunction=compare)
        analyzer['airports'] = mp.newMap(numelements=10700,  # TODO: mirar tamaño
                                         maptype='PROBING',
                                         comparefunction=compare)
        analyzer['cities'] = mp.newMap(numelements=10700,  # TODO: mirar tamaño
                                       maptype='PROBING',
                                       comparefunction=compare)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model: new_analyzer')


# Functions that add information to the analyzer


def add_airport(analyzer, airport):
    """
    Añade la abreviación AITA de cada aeropuerto en el archivo 
    airports_full.csv como un vértice del dígrafo 'digraph' del
    Analizador.
    """
    try:
        if not gr.containsVertex(analyzer['digraph'], airport['IATA']):
            gr.insertVertex(analyzer['digraph'], airport['IATA'])

        airport_exists = mp.contains(analyzer['airports'], airport['IATA'])
        if not airport_exists:
            mp.put(analyzer['airports'], airport['IATA'], airport)

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
        route_exists = mp.contains(analyzer['routes'], origin)
        if route_exists:
            route_entry = mp.get(analyzer['routes'], origin)
            array = me.getValue(route_entry)
            lt.addLast(array, destination)
        else:
            array = lt.newList(datastructure='ARRAY_LIST')
            lt.addLast(array, destination)
            mp.put(analyzer['routes'], origin, array)
    except Exception as exp:
        error.reraise(exp, 'model: add_route_digraph: put_hashtable')
    

def add_route_graph(analyzer, route):
    """
    Añade un arco origin -- destination al grafo 'graph' del Analizador,
    si y solamente si existe una ruta origin -> destination y también
    una ruta destination -> origin.
    """
    try:
        origin = route['Departure']
        destination = route['Destination']
        dist = float(route['distance_km'])
        
        destination_exists = mp.contains(analyzer['routes'], destination)
        if destination_exists:
            destination_entry = mp.get(analyzer['routes'], destination)
            array = me.getValue(destination_entry)
            if lt.isPresent(array, origin) != 0:  
                # 'origin' is in the array that is value of the key 
                # 'destination' in the hash table. Thus, there exists an
                # edge destination -> origin.
                if not gr.containsVertex(analyzer['graph'], origin):
                    gr.insertVertex(analyzer['graph'], origin)
                if not gr.containsVertex(analyzer['graph'], destination):
                    gr.insertVertex(analyzer['graph'], destination)
                edge = gr.getEdge(analyzer['graph'], origin, destination)
                if edge is None:
                    gr.addEdge(analyzer['graph'], origin, destination, dist)
                # Given that the graph is not directed, when invoking 
                # gr.addEdge(graph, origin, destination) not only an
                # edge origin -> destination is added but also an edge
                # destination -> origin. Due to that, when using
                # 'origin' and 'destination' as parameters of 
                # gr.getEdge() or gr.addEdge() their positions are 
                # interchangeable.
                return analyzer
        else:
            # If the destination doesn't exist in the hash table, there
            # is no edge destination -> origin. The execution of the
            # function ends. 
            return analyzer
    except Exception as exp:
        error.reraise(exp, 'model: add_route_graph')


def add_city(analyzer, city):
    """
    Añade una ciudad a la tabla de hash cuyas llaves son ciudades y
    cuyos valores son los diccionarios con la información de cada
    ciudad.
    """
    try:
        city_exists = mp.contains(analyzer['cities'], city['city'])
        if not city_exists:
            mp.put(analyzer['cities'], city['city'], city)
    except Exception as exp:
        error.reraise(exp, 'model: add_city')


# Load data


def info_graphs(analyzer):
    ne_digraph = gr.numEdges(analyzer['digraph'])
    nv_digraph = gr.numVertices(analyzer['digraph'])
    ne_graph = gr.numEdges(analyzer['graph'])
    nv_graph = gr.numVertices(analyzer['graph'])
    ncities = mp.size(analyzer['cities'])
    a_dg = 'FALTA'
    a_g = 'FALTA'
    city = 'FALTA'
    return ne_digraph, nv_digraph, ne_graph, nv_graph, ncities, a_dg, a_g, city


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