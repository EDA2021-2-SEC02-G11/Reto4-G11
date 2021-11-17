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
    # print('Se cargaron '+str(lt.size(catalog['sightings']))+' avistamientos ' +
    #       'de OVNIS.\n')
    # print('Primeros cinco y últimos cinco avistamientos cargados: ')
    # table = PrettyTable(['Fecha y hora', 'Ciudad', 'País', 'Duración (s)',
    #                     'Forma'])
    # ll = catalog['sightings']
    # for i in 1, 2, 3, 4, 5, -4, -3, -2, -1, 0:
    #     table.add_row([lt.getElement(ll, i)['datetime'],
    #                    lt.getElement(ll, i)['city'],
    #                    lt.getElement(ll, i)['country'],
    #                    lt.getElement(ll, i)['duration (seconds)'],
    #                    lt.getElement(ll, i)['shape']])
    # print(table)
    # return catalog


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
            cont = controller.init()
        elif inputs > 0 and inputs < 7:
            try:
                cont
            except NameError:
                print(error_cargar)
                continue
            print('Los requerimientos aún no se han implementado.')
            # if inputs == 1:
            #     print_req1(cont)
            # elif inputs == 2:
            #     print_req2(cont)
            # elif inputs == 3:
            #     print_req3(cont)
            # elif inputs == 4:
            #     print_req4(cont)
            # elif inputs == 5:
            #     print_req5(cont)
            # elif inputs == 6:
            #     print_req6(cont)
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