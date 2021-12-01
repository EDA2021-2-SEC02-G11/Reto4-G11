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
 """

import config as cf
import model
import csv


# Start Analizer.

def init():
    """ Recupera el Analizador del modelo y lo retorna."""
    analyzer = model.new_analyzer()
    return analyzer


# Load data from CSV files to Analizer.

def load_data(analyzer):
    """
    Carga los datos de los archivos CSV al analizador en el modelo.
    """
    data = cf.data_dir + 'Skylines/'
    airports_file = csv.DictReader(open(data + 'airports_full.csv',
                                        encoding="utf-8"), delimiter=",")
    routes_file = csv.DictReader(open(data + 'routes_full.csv',
                                      encoding="utf-8"), delimiter=",")
    worldcities_file = csv.DictReader(open(data + 'worldcities.csv',
                                           encoding="utf-8"), delimiter=",")
    for airport in airports_file:
        model.add_airport(analyzer, airport)
    for route in routes_file:
        model.add_route_digraph(analyzer, route)
        model.add_route_graph(analyzer, route)
    for city in worldcities_file:
        model.add_city(analyzer, city)
    return analyzer


# Functions that connect view to model


def info_graphs(analyzer):
    return model.info_graphs(analyzer)


def requirement1(analyzer):
    return model.requirement1(analyzer)


def requirement2(analizer, iata1, iata2):
    return model.requirement2(analizer, iata1, iata2)


def homonym_cities(analyzer, city):
    return model.homonym_cities(analyzer, city)


def requirement3(analyzer, origin_dict, destiny_dict):
    return model.requirement3(analyzer, origin_dict, destiny_dict)


def requirement4(analyzer):
    return model.requirement4(analyzer)


def requirement5(analyzer):
    return model.requirement5(analyzer)


def requirement6(analyzer):
    return model.requirement6(analyzer)
