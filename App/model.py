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
# from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Graphs import scc
# from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
import numpy as np
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
            ciudades y como valores una lista con el diccionario con la 
            información de la ciudad. Si varias ciudades son homónimas, 
            la lista contiene los diccionarios con la información
            de las ciudades.
    loaded: Estructura que almacena qué aeropuerto se cargó
            primero a cada grafo y qué ciudad se cargó última.

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
                    'loaded': {},
                    'components': None,
                    'paths': None
                    }

        analyzer['digraph'] = gr.newGraph(datastructure='ADJ_LIST',
                                          directed=True,
                                          size=10700,
                                          comparefunction=comparek)
        analyzer['graph'] = gr.newGraph(datastructure='ADJ_LIST',
                                        directed=False,
                                        size=4000,
                                        comparefunction=comparek)
        analyzer['routes'] = mp.newMap(numelements=10700,
                                       maptype='PROBING',
                                       comparefunction=comparek)
        analyzer['airports'] = mp.newMap(numelements=10700,
                                         maptype='PROBING',
                                         comparefunction=comparek)
        analyzer['cities'] = mp.newMap(numelements=37500,
                                       maptype='PROBING',
                                       comparefunction=comparek)
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
        # Add vertex to digraph
        if not gr.containsVertex(analyzer['digraph'], airport['IATA']):
            gr.insertVertex(analyzer['digraph'], airport['IATA'])

        # Add airport to hash table
        airport_exists = mp.contains(analyzer['airports'], airport['IATA'])
        if not airport_exists:
            mp.put(analyzer['airports'], airport['IATA'], airport)

        # First airport loaded to digraph
        if 'first_digraph' not in analyzer['loaded']:
            analyzer['loaded']['first_digraph'] = airport

    except Exception as exp:
        error.reraise(exp, 'model: add_airport')


def add_route_digraph(analyzer, route):
    """
    Añade un arco dirigido al dígrafo 'digraph' del Analizador.
    """
    # Add edge to digraph
    try:
        origin = route['Departure']
        destination = route['Destination']
        distance = float(route['distance_km'])
        edge = gr.getEdge(analyzer['digraph'], origin, destination)
        if edge is None:
            gr.addEdge(analyzer['digraph'], origin, destination, distance)
    except Exception as exp:
        error.reraise(exp, 'model: add_route_digraph: add_edge')

    # Add destination from route to destination list in hash table
    try:
        route_exists = mp.contains(analyzer['routes'], origin)
        if route_exists:
            route_entry = mp.get(analyzer['routes'], origin)
            array = me.getValue(route_entry)
            if lt.isPresent(array, destination) == 0:
                lt.addLast(array, destination)
        else:
            array = lt.newList(datastructure='ARRAY_LIST', cmpfunction=compare)
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

                # First airport loaded to graph
                if 'first_graph' not in analyzer['loaded']:
                    entry = mp.get(analyzer['airports'], origin)
                    airport = me.getValue(entry)
                    analyzer['loaded']['first_graph'] = airport

    except Exception as exp:
        error.reraise(exp, 'model: add_route_graph')


def add_city(analyzer, city):
    """
    Añade una ciudad a la tabla de hash cuyas llaves son ciudades y
    cuyos valores son los diccionarios con la información de cada
    ciudad.
    """
    try:
        # Add city to hash table
        city_exists = mp.contains(analyzer['cities'], city['city'])
        if not city_exists:
            homonyms = lt.newList()
            lt.addLast(homonyms, city)
            mp.put(analyzer['cities'], city['city'], homonyms)
        else:
            homonyms = me.getValue(mp.get(analyzer['cities'], city['city']))
            lt.addLast(homonyms, city)

        # Last city loaded
        analyzer['loaded']['last_city'] = city

    except Exception as exp:
        error.reraise(exp, 'model: add_city')


# Load data


def info_graphs(analyzer):
    Ne_di = gr.numEdges(analyzer['digraph'])
    Nv_di = gr.numVertices(analyzer['digraph'])
    Ne_graph = gr.numEdges(analyzer['graph'])
    Nv_graph = gr.numVertices(analyzer['graph'])
    Ncities = mp.size(analyzer['cities'])
    Nhom = 41002  # TODO
    a_dg = analyzer['loaded']['first_digraph']
    a_g = analyzer['loaded']['first_graph']
    city = analyzer['loaded']['last_city']
    return Ne_di, Nv_di, Ne_graph, Nv_graph, Ncities, Nhom, a_dg, a_g, city


# Requirements


def requirement1(analyzer):
    pass


def requirement2(analyzer, iata1, iata2):
    N_scc = scc.connectedComponents(scc.KosarajuSCC(analyzer['digraph']))
    bool_scc = scc.stronglyConnected(scc.KosarajuSCC(analyzer['digraph']),
                                     iata1, iata2)
    if bool_scc is True:
        si_no_scc = 'sí'
    elif bool_scc is True:
        si_no_scc = 'no'
    return N_scc, si_no_scc


def homonym_cities(analyzer, city):
    map = analyzer['cities']
    if mp.contains(map, city):
        value = me.getValue(mp.get(map, city))
        if lt.size(value) == 1:
            return 1, lt.getElement(value, 1)
        else:  # The value is a list of dictionaries
            return lt.size(value), value


def requirement3(analyzer, origin_dict, destiny_dict):
    print(origin_dict)
    print(destiny_dict)

def haversine(lon1, lat1, lon2, lat2):
    """
    Calcula la distancia harvesiana entre dos puntos  
    """
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = np.sin(dlat/2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2.0)**2

    c = 2 * np.arcsin(np.sqrt(a))
    km = 6367 * c
    return km

def requirement4(analyzer):
    pass


def requirement5(analyzer):
    pass


def requirement6(analyzer):
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


def comparek(thing1, key1):
    """
    Compara dos estaciones
    """
    thing2 = key1['key']
    return compare(thing1, thing2)
