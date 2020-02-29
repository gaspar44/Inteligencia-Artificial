# This file contains all the required routines to make an A* search algorithm.
#
__authors__ = '1499617'
__group__ = 'DM.18'

# _________________________________________________________________________________________
# Intel.ligencia Artificial
# Grau en Enginyeria Informatica
# Curs 2016- 2017
# Universitat Autonoma de Barcelona
# _______________________________________________________________________________________

from SubwayMap import *
from utils import *
import copy


def expand(path, map):
    """
     It expands a SINGLE station and returns the list of class Path.
     Format of the parameter is:
        Args:
            path (object of Path class): Specific path to be expanded
            map (object of Map class):: All the information needed to expand the node
        Returns:
            path_list (list): List of paths that are connected to the given path.
    """
    element_to_start_search = path.last
    path_to_return = []

    for key in map.connections[element_to_start_search]:
        path_base_element = copy.deepcopy(path) if len(path.route) > 1 else Path(element_to_start_search)
        path_base_element.add_route(key)
        path_base_element.update_g(map.connections[element_to_start_search][key])
        path_base_element.update_f()
        path_to_return.append(path_base_element)

    return path_to_return

def remove_cycles(path_list):
    """
     It removes from path_list the set of paths that include some cycles in their path.
     Format of the parameter is:
        Args:
            path_list (LIST of Path Class): Expanded paths
        Returns:
            path_list (list): Expanded paths without cycles.
    """

    removed_cycles_paths = []
    for i in range(len(path_list)):
        actual_element = path_list[i].route
        if all(actual_element[x] not in actual_element[x + 1:] for x in range(len(actual_element))):
            auxiliar_path = copy.deepcopy(path_list[i])
            removed_cycles_paths.append(auxiliar_path)

    return removed_cycles_paths


def insert_depth_first_search(expand_paths, list_of_path):
    """
     expand_paths is inserted to the list_of_path according to DEPTH FIRST SEARCH algorithm
     Format of the parameter is:
        Args:
            expand_paths (LIST of Path Class): Expanded paths
            list_of_path (LIST of Path Class): The paths to be visited
        Returns:
            list_of_path (LIST of Path Class): List of Paths where Expanded Path is inserted
    """
    list_of_path_to_return = []
    if expand_paths:
        for i in range(len(expand_paths)-1, -1, -1):
            auxPath = copy.deepcopy(expand_paths[i])
            list_of_path_to_return.insert(0, auxPath)
        return list_of_path_to_return

    else:
        list_of_path_to_return = copy.deepcopy(list_of_path)
        list_of_path_to_return.pop(0)
        return list_of_path_to_return


def depth_first_search(origin_id, destination_id, map):
    """
     Depth First Search algorithm
     Format of the parameter is:
        Args:
            origin_id (int): Starting station id
            destination_id (int): Final station id
            map (object of Map class): All the map information
        Returns:
            list_of_path[0] (Path Class): the route that goes from origin_id to destination_id
    """
    list_of_path = [Path(origin_id)]

    while len(list_of_path) != 0 and destination_id not in list_of_path[0].route:
        first_element_list = list_of_path[0]
        expanded_path = expand(first_element_list, map)
        expanded_path = remove_cycles(expanded_path)
        list_of_path = insert_depth_first_search(expanded_path, list_of_path)

    return list_of_path[0]


def insert_breadth_first_search(expand_paths, list_of_path):
    """
        expand_paths is inserted to the list_of_path according to BREADTH FIRST SEARCH algorithm
        Format of the parameter is:
           Args:
               expand_paths (LIST of Path Class): Expanded paths
               list_of_path (LIST of Path Class): The paths to be visited
           Returns:
               list_of_path (LIST of Path Class): List of Paths where Expanded Path is inserted
    """
    list_of_path_to_return = copy.deepcopy(list_of_path)
    list_of_path_to_return.pop(0)

    if expand_paths:
        for i in range(len(expand_paths)-1, -1, -1):
            auxPath = copy.deepcopy(expand_paths[i])
            list_of_path_to_return.append(auxPath)

    return list_of_path_to_return


def breadth_first_search(origin_id, destination_id, map):
    """
     Breadth First Search algorithm
     Format of the parameter is:
        Args:
            origin_id (int): Starting station id
            destination_id (int): Final station id
            map (object of Map class): All the map information
        Returns:
            list_of_path[0] (Path Class): The route that goes from origin_id to destination_id
    """

    list_of_path = [Path(origin_id)]

    while len(list_of_path) != 0 and destination_id not in list_of_path[0].route:
        first_element_list = list_of_path[0]
        expanded_path = expand(first_element_list, map)
        expanded_path = remove_cycles(expanded_path)
        list_of_path = insert_breadth_first_search(expanded_path, list_of_path)

    return list_of_path[0]

def calculate_cost(expand_paths, map, type_preference=0):
    """
         Calculate the cost according to type preference
         Format of the parameter is:
            Args:
                expand_paths (LIST of Paths Class): Expanded paths
                map (object of Map class): All the map information
                type_preference: INTEGER Value to indicate the preference selected:
                                0 - Adjacency
                                1 - minimum Time
                                2 - minimum Distance
                                3 - minimum Transfers
            Returns:
                expand_paths (LIST of Paths): Expanded path with updated cost
    """
    pass


def insert_cost(expand_paths, list_of_path):
    """
        expand_paths is inserted to the list_of_path according to COST VALUE
        Format of the parameter is:
           Args:
               expand_paths (LIST of Path Class): Expanded paths
               list_of_path (LIST of Path Class): The paths to be visited
           Returns:
               list_of_path (LIST of Path Class): List of Paths where expanded_path is inserted according to cost
    """
    pass


def uniform_cost_search(origin_id, destination_id, map, type_preference=0):
    """
     Uniform Cost Search algorithm
     Format of the parameter is:
        Args:
            origin_id (int): Starting station id
            destination_id (int): Final station id
            map (object of Map class): All the map information
        Returns:
            list_of_path[0] (Path Class): The route that goes from origin_id to destination_id
    """
    pass


def calculate_heuristics(expand_paths, map, destination_id, type_preference=0):
    """
     Calculate and UPDATE the heuristics of a path according to type preference
     WARNING: In calculate_cost, we didn't update the cost of the path inside the function
              for the reasons which will be clear when you code Astar (HINT: check remove_redundant_paths() function).
     Format of the parameter is:
        Args:
            expand_paths (LIST of Path Class): Expanded paths
            map (object of Map class): All the map information
            type_preference: INTEGER Value to indicate the preference selected:
                            0 - Adjacency
                            1 - minimum Time
                            2 - minimum Distance
                            3 - minimum Transfers
        Returns:
            expand_paths (LIST of Path Class): Expanded paths with updated heuristics
    """
    pass


def update_f(expand_paths):
    """
      Update the f of a path
      Format of the parameter is:
         Args:
             expand_paths (LIST of Path Class): Expanded paths
         Returns:
             expand_paths (LIST of Path Class): Expanded paths with updated costs
    """
    pass


def remove_redundant_paths(expand_paths, list_of_path, visited_stations_cost):
    """
      It removes the Redundant Paths. They are not optimal solution!
      If a station is visited and have a lower g in this moment, we should remove this path.
      Format of the parameter is:
         Args:
             expand_paths (LIST of Path Class): Expanded paths
             list_of_path (LIST of Path Class): All the paths to be expanded
             visited_stations_cost (dict): All visited stations cost
         Returns:
             new_paths (LIST of Path Class): Expanded paths without redundant paths
             list_of_path (LIST of Path Class): list_of_path without redundant paths
    """
    pass


def insert_cost_f(expand_paths, list_of_path):
    """
        expand_paths is inserted to the list_of_path according to f VALUE
        Format of the parameter is:
           Args:
               expand_paths (LIST of Path Class): Expanded paths
               list_of_path (LIST of Path Class): The paths to be visited
           Returns:
               list_of_path (LIST of Path Class): List of Paths where expanded_path is inserted according to f
    """
    pass


def min_distance_stations(candidates_to_min_distance):
    smallest_value = np.min(list(candidates_to_min_distance.values()))
    stationsID = []

    for key in candidates_to_min_distance:
        if candidates_to_min_distance[key] == smallest_value:
            stationsID.append(key)

    return stationsID


def coord2station(coord, map):
    """
        From coordinates, it searches the closest station.
        Format of the parameter is:
        Args:
            coord (list):  Two REAL values, which refer to the coordinates of a point in the city.
            map (object of Map class): All the map information
        Returns:
            possible_origins (list): List of the Indexes of stations, which corresponds to the closest station
    """
    candidates_to_min_distance = {}
    for key in map.stations:
        x_side = (coord[0] - map.stations[key]['x']) ** 2
        y_side = (coord[1] - map.stations[key]['y']) ** 2
        distance = math.sqrt(x_side + y_side)
        candidates_to_min_distance[key] = distance

    return min_distance_stations(candidates_to_min_distance)


def Astar(origin_coor, dest_coor, map, type_preference=0):
    """
     A* Search algorithm
     Format of the parameter is:
        Args:
            origin_id (list): Starting station id
            destination_id (int): Final station id
            map (object of Map class): All the map information
            type_preference: INTEGER Value to indicate the preference selected:
                            0 - Adjacency
                            1 - minimum Time
                            2 - minimum Distance
                            3 - minimum Transfers
        Returns:
            list_of_path[0] (Path Class): The route that goes from origin_id to destination_id
    """
    pass
