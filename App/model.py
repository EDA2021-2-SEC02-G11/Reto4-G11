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
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
# from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Graphs import scc
from DISClib.Utils import error as error
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Algorithms.Graphs import prim as prim
from math import radians, cos, sin, asin, sqrt
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
                    'airports_tree': None,
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
        analyzer['airports'] = mp.newMap(numelements=10700,
                                         maptype='PROBING',
                                         comparefunction=comparek)
        analyzer['cities'] = mp.newMap(numelements=37500,
                                       maptype='PROBING',
                                       comparefunction=comparek)
        analyzer['airports_tree'] = om.newMap(omaptype='RBT',
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
        # Add vertex to digraph
        if not gr.containsVertex(analyzer['digraph'], airport['IATA']):
            gr.insertVertex(analyzer['digraph'], airport['IATA'])

        # Add vertex to graph
        if not gr.containsVertex(analyzer['graph'], airport['IATA']):
            gr.insertVertex(analyzer['graph'], airport['IATA'])

        # Add airport to hash table
        airport_exists = mp.contains(analyzer['airports'], airport['IATA'])
        if not airport_exists:
            mp.put(analyzer['airports'], airport['IATA'], airport)

        # Add airport to airports tree
        create_airports_tree(analyzer, airport)

        # First and last airport loaded to digraph
        if 'first_digraph' not in analyzer['loaded']:
            analyzer['loaded']['first_digraph'] = airport
        analyzer['loaded']['last_digraph'] = airport

        # First and last airport loaded to graph
        if 'first_graph' not in analyzer['loaded']:
            analyzer['loaded']['first_graph'] = airport
        analyzer['loaded']['last_graph'] = airport

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
        digraph = analyzer['digraph']
        if gr.getEdge(digraph, origin, destination) is None:
            gr.addEdge(analyzer['digraph'], origin, destination, distance)
    except Exception as exp:
        error.reraise(exp, 'model: add_route_digraph: add_edge')


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
        digraph = analyzer['digraph']
        if gr.getEdge(digraph, origin, destination) is not None and \
           gr.getEdge(digraph, destination, origin) is not None:
            if gr.getEdge(analyzer['graph'], origin, destination) is None:
                gr.addEdge(analyzer['graph'], origin, destination, dist)
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

        # First and last city loaded
        if 'first_city' not in analyzer['loaded']:
            analyzer['loaded']['first_city'] = city
        analyzer['loaded']['last_city'] = city

    except Exception as exp:
        error.reraise(exp, 'model: add_city')


def create_airports_tree(analyzer, airport):
    """
    Crea el árbol de aeropuertos.
    El árbol tiene como llaves la coordenada latitud (aproximada a dos cifras
    decimales) y como valores árboles. Cada árbol tiene como llaves
    coordenadas de longitud (aproximadas a dos cifras decimales) y como valor
    para cada llave el aeropuerto ubicado en la latitud y longitud dadas.
    """
    lat_tree = analyzer['airports_tree']
    lat_tree_entry = om.get(lat_tree, float(airport['Latitude']))
    if lat_tree_entry is None:
        long_tree = om.newMap(omaptype='RBT', comparefunction=compare)
        om.put(long_tree, float(airport['Longitude']), airport)
        om.put(lat_tree, float(airport['Latitude']), long_tree)
    else:
        long_tree = me.getValue(lat_tree_entry)
        long_tree_entry = om.get(long_tree, float(airport['Longitude']))
        if long_tree_entry is None:
            om.put(long_tree, float(airport['Longitude']), airport)
    return lat_tree


# Load data


def count_cities(analyzer, count):
    analyzer['loaded']['N_cities'] = count


def info_graphs(analyzer):
    loaded = analyzer['loaded']
    loaded['N_edges_digraph'] = gr.numEdges(analyzer['digraph'])
    loaded['N_vertices_digraph'] = gr.numVertices(analyzer['digraph'])
    loaded['N_edges_graph'] = gr.numEdges(analyzer['graph'])
    loaded['N_vertices_graph'] = gr.numVertices(analyzer['graph'])
    loaded['N_dif_cities'] = mp.size(analyzer['cities'])
    return loaded


# Requirements


def requirement1(analyzer):
    digraph = analyzer['digraph']
    N_connected = 0
    scooby = {}
    for vertex in lt.iterator(gr.vertices(digraph)):
        inde=gr.indegree(digraph, vertex)
        outde=gr.outdegree(digraph, vertex)
        degree_ = gr.indegree(digraph, vertex) + gr.outdegree(digraph, vertex)
        if degree_ > 0:
            N_connected += 1
            scooby[vertex] = [degree_,inde,outde]
    tops=[]
    for i in range(0,5):
        top=0
        aer=""
        for i in scooby.keys():
            if scooby[i][0]>top and i not in tops:
                top=scooby[i][0]
                aer=i
        tops.append(aer)
    res={}
    for i in tops:
        res[i]=[me.getValue(mp.get(analyzer['airports'], i)),scooby[i]]

    # Incompleta. Terminar.
    return N_connected,res,tops


def requirement2(analyzer, iata1, iata2):
    N_scc = scc.connectedComponents(scc.KosarajuSCC(analyzer['digraph']))
    bool_scc = scc.stronglyConnected(scc.KosarajuSCC(analyzer['digraph']),
                                     iata1, iata2)
    aer1=me.getValue(mp.get(analyzer['airports'], iata1))
    aer2=me.getValue(mp.get(analyzer['airports'], iata2))
    return N_scc, bool_scc,aer1,aer2


def homonym_cities(analyzer, city):
    map = analyzer['cities']
    if mp.contains(map, city):
        value = me.getValue(mp.get(map, city))
        if lt.size(value) == 1:
            return 1, lt.getElement(value, 1)
        else:  # The value is a list of dictionaries
            return lt.size(value), value


def requirement3(analyzer, origin_dict, destiny_dict):
    origen = cuadrado(analyzer, origin_dict)
    print(origen)
    destino = cuadrado(analyzer, destiny_dict)
    aerOrigen = nearAirport(origen, origin_dict)
    aerDestino = nearAirport(destino, destiny_dict)
    print(aerOrigen," hola")
    print(aerDestino)
    search = djk.Dijkstra(analyzer['graph'], "LED")
    print(djk.hasPathTo(search,aerDestino["IATA"]))
    if djk.hasPathTo(search,aerDestino["IATA"])==True:
        path=djk.pathTo(search,aerDestino["IATA"])
        print(path)
        print(str(djk.distTo(search,aerDestino["IATA"])))
        dist = str(djk.distTo(search,aerDestino["IATA"]))
        stops = {}
    else:
        path={}
        dist=0
        stops={}
    return aerOrigen, aerDestino, dist, path, stops


def nearAirport(list_airports, city_dict):
    if lt.size(list_airports) > 1:
        menor = float("inf")
        for i in lt.iterator(list_airports):
            harvesiana = haversine(float(city_dict["lng"]),
                                   float(city_dict["lat"]),
                                   float(i["Longitude"]), float(i["Latitude"]))
            if harvesiana < menor:
                menor = harvesiana
                airport = i
    else:
        airport = lt.getElement(list_airports, 1)
    return airport


def cuadrado(analyzer, origin_dict):
    sample = lt.newList(datastructure='ARRAY_LIST')
    tree = analyzer["airports_tree"]
    lat = float(origin_dict["lat"])
    lon = float(origin_dict["lng"])
    medida_cuadrado = 0.01  # 0.01 degrees = approximately 10 km
    lat_max = lat+medida_cuadrado
    lat_min = lat-medida_cuadrado
    i = False
    while i is False:
        range_lat = om.values(tree, lat_min, lat_max)
        j = 1
        lon_max = lon+medida_cuadrado
        lon_min = lon-medida_cuadrado
        while j <= lt.size(range_lat):
            lon_tree = lt.getElement(range_lat, j)
            values_lon_tree = om.values(lon_tree, lon_min, lon_max)
            k = 1
            while k <= lt.size(values_lon_tree):
                airport = lt.getElement(values_lon_tree, k)
                lt.addLast(sample, airport)
                i = True
                k += 1
            lon_max += medida_cuadrado
            lon_min -= medida_cuadrado
            j += 1
        lat_max += medida_cuadrado
        lat_min -= medida_cuadrado
    return sample


def haversine(lon1, lat1, lon2, lat2):
    """
    Calcula la distancia entre dos puntos utilizando la Fórmula del
    semiverseno.
    """
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    km = 6367 * c
    return km


def requirement4(analyzer,IATA,miles):
    # MST con grafo no dirigido
    maxi=0
    search=prim.PrimMST(analyzer["digraph"])
    bus=prim.prim(analyzer["digraph"],search,IATA)
    #print(search)
    print(bus)
    return search, bus


def requirement5(analyzer):
    #Encontrar los adjacentes o por los que es adjacente y luego pasar a ciudades
    pass


def requirement6(analyzer):
    pass

def requirement7(analyzer):
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
