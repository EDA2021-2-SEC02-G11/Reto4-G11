﻿"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
 """

import threading
import config as cf
import sys
import controller
from prettytable import PrettyTable
from DISClib.ADT import list as lt
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""


# Menú y cargar datos.


def print_menu():
    """
    Imprime las opciones del menú.
    """
    print('\nBienvenido al menú.\n')
    print('0. Cargar datos y generar el catálogo.')
    print('1. Encontrar puntos de interconexión aérea.')
    print('2. Encontrar clústeres de tráfico aéreo.')
    print('3. Encontrar la ruta más corta entre ciudades.')
    print('4. Utilizar las millas de viajero.')
    print('5. Cuantificar el efecto de un aeropuerto cerrado.')
    print('6. Comparar con servicio WEB externo.')
    print('7. Detener la ejecución del programa.')


def print_load_data():
    print('Cargando información de los archivos...\n')
    analyzer = controller.init()
    controller.load_data(analyzer)
    r = controller.info_graphs(analyzer)
    Ne_di, Nv_di, Ne_graph, Nv_graph, Ncities, Nhom, a_dg, a_g, city = r

    # Digraph
    print('\nEn el dígrafo hay un total de '+str(Nv_di) +
          ' aeropuertos con abreviación IATA única.')
    print('En el dígrafo hay un total de '+str(Ne_di) +
          ' rutas aéreas dirigidas únicas.\n')
    print('Información del primer aeropuerto cargado en el dígrafo:')
    table1 = PrettyTable(['Nombre', 'Ciudad', 'País', 'Latitud',
                         'Longitud'])
    table1.add_row([a_dg['Name'],
                    a_dg['City'],
                    a_dg['Country'],
                    a_dg['Latitude'],
                    a_dg['Longitude']])
    print(table1)

    # Graph
    print('\nEn el grafo no dirigido hay un total de '+str(Nv_graph) +
          ' aeropuertos con abreviación IATA única.')
    print('En el grafo no dirigido hay un total de '+str(Ne_graph) +
          ' rutas aéreas bidireccionales únicas.\n')
    print('Información del primer aeropuerto cargado en el grafo no dirigido:')
    table2 = PrettyTable(['Nombre', 'Ciudad', 'País', 'Latitud',
                         'Longitud'])
    table2.add_row([a_g['Name'],
                    a_g['City'],
                    a_g['Country'],
                    a_g['Latitude'],
                    a_g['Longitude']])
    print(table2)

    # Cities
    print('Hay un total de '+str(Ncities)+' ciudades con nombres distintos. ' +
          'Contando las ciudades homónimas, hay '+str(Nhom)+' ciudades.\n')
    print('Información de la última ciudad cargada:')
    table3 = PrettyTable(['Ciudad', 'Población', 'Latitud',
                         'Longitud'])
    table3.add_row([city['city'],
                    city['population'],
                    city['lat'],
                    city['lng']])
    print(table3)
    return analyzer


catalog = None


def print_req1(analyzer):
    num_digraph, num_graph = controller.requirement2(analyzer)
    # Digraph
    print('Los aeropuertos que sirven como punto de interconexión a más ' +
          'rutas aéreas en el dígrafo son:')
    # TODO: Lista de aeropuertos (IATA, nombre, ciudad, país).
    print('Cada uno se interconecta con '+str(num_digraph)+'aeropuertos')

    # Graph
    print('Los aeropuertos que sirven como punto de interconexión a más ' +
          'rutas aéreas en el grafo no dirigido son:')
    # TODO: Lista de aeropuertos (IATA, nombre, ciudad, país).
    print('Cada uno se interconecta con '+str(num_graph)+'aeropuertos')


def print_req2(analyzer):
    iata1 = input('Ingrese el código IATA del primer aeropuerto: ')
    iata2 = input('Ingrese el código IATA del segundo aeropuerto: ')
    N_scc, si_no_scc = controller.requirement2(analyzer, iata1, iata2)
    print('El número de clústeres presentes en la red de transporte aéreo, ' +
          'que es el número de componentes fuertemente conectados en el ' +
          'dígrafo, es'+str(N_scc))
    print('Los dos aeropuertos ingresados, '+str(iata1)+' y '+str(iata2)+', ' +
          str(si_no_scc)+'están en el mismo clúster.')


def choose_homonym(hl):
    """
    Imprime una lista de ciudades homónimas con información del país, la
    subregión (departamento, estado o prefectura) y la ubicación
    geográfica (latitud y longitud) de cada una para que el usuario
    pueda elegir entre ellas. retorna el diccionario con la información
    de la ciudad elegida por el usuario.
    """
    table = PrettyTable(['Número', 'Ciudad', 'País', 'Subregión', 'Latitud',
                        'Longitud'])
    for i in range(1, lt.size(hl)+1):
        table.add_row([str(i),
                      lt.getElement(hl, i)['city'],
                      lt.getElement(hl, i)['country'],
                      lt.getElement(hl, i)['admin_name'].title(),
                      lt.getElement(hl, i)['lat'].title(),
                      lt.getElement(hl, i)['lng']])
    print(table)
    choice = int(input('Ingrese el número de la ciudad a la que se refiere: '))
    dict_city = lt.getElement(hl, choice)
    return dict_city


def print_req3(analyzer):
    origin = input('Ingrese la ciudad de origen: ')
    destiny = input('Ingrese la ciudad de destino: ')
    N_hom_origin, origin_list = controller.homonym_cities(analyzer, origin)
    N_hom_destiny, destiny_list = controller.homonym_cities(analyzer, destiny)
    if N_hom_origin > 1:
        print('Hay '+str(N_hom_origin)+' ciudades homónimas a '+str(origin) +
              '. Elija a cuál ciudad se refiere del siguiente listado:')
        origin_dict = choose_homonym(origin_list)
    if N_hom_destiny > 1:
        print('Hay '+str(N_hom_destiny)+' ciudades homónimas a '+str(destiny) +
              '. Elija a cuál ciudad se refiere del siguiente listado:')
        destiny_dict = choose_homonym(destiny_list)
    if (N_hom_origin == 1) and (N_hom_destiny == 1):
        print('No hay ciudades homónimas a ninguna de las ingresadas')
        # As there are no homonyms, 'homonym_cities' returns
        # dictionaries, not lists
        origin_dict = origin_list
        destiny_dict = destiny_list
    controller.requirement3(analyzer, origin_dict, destiny_dict)


"""
Menú principal
"""


def thread_cycle():
    while True:
        error = '\nError: Por favor ingrese un número entero entre 0 y 7.\n'
        error_cargar = ('\nError: Se deben cargar los datos antes de usar ' +
                        'los requisitos.\n')
        print_menu()
        try:
            inputs = int(input('Seleccione una opción para continuar:\n> '))
        except Exception:
            print(error)
            continue
        if inputs == 0:
            analyzer = print_load_data()
        elif inputs > 0 and inputs < 7:
            try:
                analyzer
            except NameError:
                print(error_cargar)
                continue
            print('Los requerimientos aún no se han implementado.')
            if inputs == 1:
                print_req1(analyzer)
            elif inputs == 2:
                print_req2(analyzer)
            elif inputs == 3:
                print_req3(analyzer)
            # elif inputs == 4:
            #     print_req4(analyzer)
            # elif inputs == 5:
            #     print_req5(analyzer)
            # elif inputs == 6:
            #     print_req6(analyzer)
        elif inputs > 7:
            print(error)
        else:
            sys.exit(0)
    sys.exit(0)


if __name__ == "__main__":
    threading.stack_size(67108864)  # 64MB stack
    sys.setrecursionlimit(2 ** 20)
    thread = threading.Thread(target=thread_cycle)
    thread.start()
