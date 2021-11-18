"""
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
# from DISClib.ADT import list as lt
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
    ne_digraph, nv_digraph, ne_graph, nv_graph, ncities, a_dg, a_g, city = r
    # Digraph
    print('\nEn el dígrafo hay un total de '+str(nv_digraph) +
          ' aeropuertos con abreviación IATA única.')
    print('En el dígrafo hay un total de '+str(ne_digraph) +
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
    print('\nEn el grafo hay un total de '+str(nv_graph) +
          ' aeropuertos con abreviación IATA única.')
    print('En el grafo hay un total de '+str(ne_graph) +
          ' rutas aéreas bidireccionales únicas.\n')
    print('Información del primer aeropuerto cargado en el grafo:')
    table2 = PrettyTable(['Nombre', 'Ciudad', 'País', 'Latitud',
                         'Longitud'])
    table2.add_row([a_g['Name'],
                    a_g['City'],
                    a_g['Country'],
                    a_g['Latitude'],
                    a_g['Longitude']])
    print(table2)
    # Cities
    print('Hay un total de '+str(ncities)+' ciudades.\n')
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
            inputs = int(input('Seleccione una opción para continuar:\n>'))
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
            # if inputs == 1:
            #     print_req1(analyzer)
            # elif inputs == 2:
            #     print_req2(analyzer)
            # elif inputs == 3:
            #     print_req3(analyzer)
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
