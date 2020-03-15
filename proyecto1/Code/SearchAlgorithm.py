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
            removed_cycles_paths.append(path_list[i])

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
    list_of_path_to_return = copy.deepcopy(list_of_path)
    list_of_path_to_return.pop(0)

    if expand_paths:
        for i in range(len(expand_paths) - 1, -1, -1):
            list_of_path_to_return.insert(0, expand_paths[i])

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
        for i in range(len(expand_paths) - 1, -1, -1):
            list_of_path_to_return.append(expand_paths[i])

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
    if type_preference == 0:
        for path in expand_paths:
            path.update_g(1)

    elif type_preference == 1:
        for path in expand_paths:
            first_dictionary = map.connections[path.penultimate]
            value_to_update = first_dictionary[path.last]
            path.update_g(value_to_update)

    elif type_preference == 2:
        for path in expand_paths:
            first_dictionary = map.connections[path.penultimate]
            travel_time = first_dictionary[path.last]
            actual_subway_line = map.stations[path.last]["line"]
            velocity = map.velocity[actual_subway_line]
            previous_subway_line_name = map.stations[path.penultimate]["name"]
            actual_subway_line_name = map.stations[path.last]["name"]

            distance = travel_time * velocity if actual_subway_line_name != previous_subway_line_name else 0
            path.update_g(distance)

    elif type_preference == 3:
        for path in expand_paths:
            lines_visited_until_now = [map.stations[path.head]["line"]]
            first_dictionary = map.stations[path.last]
            if first_dictionary["line"] not in lines_visited_until_now:
                lines_visited_until_now.append(first_dictionary["line"])

            path.update_g(len(lines_visited_until_now) - 1)

    return expand_paths


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

    list_of_path_to_return = copy.deepcopy(list_of_path)
    list_of_path_to_return.pop(0)

    if expand_paths:
        for i in range(len(expand_paths)):
            list_of_path_to_return.append(expand_paths[i])

    list_of_path_to_return = sorted(list_of_path_to_return, key=lambda path: path.g)
    return list_of_path_to_return


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

    list_of_path = [Path(origin_id)]

    while len(list_of_path) != 0 and destination_id not in list_of_path[0].route:
        first_element_list = list_of_path[0]
        expanded_path = expand(first_element_list, map)
        expanded_path = remove_cycles(expanded_path)
        expanded_path = calculate_cost(expanded_path, map, type_preference)
        list_of_path = insert_cost(expanded_path, list_of_path)

    return list_of_path[0]


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

    if type_preference == 0:
        for path in expand_paths:
            path.update_h(0) if path.last == destination_id else path.update_h(1)

    elif type_preference == 1 or type_preference == 2:
        for path in expand_paths:
            max_speed = max(map.velocity.values())
            coord_of_destination_station = [map.stations[destination_id]["x"], map.stations[destination_id]["y"]]
            distance = calculate_distance(coord_of_destination_station, path.last, map)
            velocity = distance / max_speed
            path.update_h(velocity) if type_preference == 1 else path.update_h(distance)

    elif type_preference == 3:
        destination_line = map.stations[destination_id]["line"]
        for path in expand_paths:
            path.update_h(0) if destination_line == map.stations[path.last]["line"] else path.update_h(1)

    return expand_paths


def update_f(expand_paths):
    """
      Update the f of a path
      Format of the parameter is:
         Args:
             expand_paths (LIST of Path Class): Expanded paths
         Returns:
             expand_paths (LIST of Path Class): Expanded paths with updated costs
    """

    for path in expand_paths:
        path.update_f()

    return expand_paths


def fix_path(last, new_paths):
    for path in new_paths:
        if last in path.route:
            new_paths.remove(path)

    return new_paths


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
    new_paths = copy.deepcopy(list_of_path)

    for path in expand_paths:
        if path.last not in visited_stations_cost:
            visited_stations_cost[path.last] = path.g

        elif path.g < visited_stations_cost[path.last]:
            visited_stations_cost[path.last] = path.g
            new_paths = fix_path(path.last, new_paths)

        else:
            expand_paths.remove(path)

    return expand_paths, new_paths, visited_stations_cost


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
    list_of_path_to_return = copy.deepcopy(list_of_path)
    list_of_path_to_return.pop(0)

    if expand_paths:
        for i in range(len(expand_paths)):
            list_of_path_to_return.append(expand_paths[i])

    list_of_path_to_return = sorted(list_of_path_to_return, key=lambda path: path.f)
    return list_of_path_to_return


def min_distance_stations(candidates_to_min_distance):
    smallest_value = np.min(list(candidates_to_min_distance.values()))
    stationsID = []

    for key in candidates_to_min_distance:
        if candidates_to_min_distance[key] == smallest_value:
            stationsID.append(key)

    return stationsID


def calculate_distance(coord, key, map):
    x_side = (coord[0] - map.stations[key]['x']) ** 2
    y_side = (coord[1] - map.stations[key]['y']) ** 2
    return math.sqrt(x_side + y_side)


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
        distance = calculate_distance(coord, key, map)
        candidates_to_min_distance[key] = distance

    return min_distance_stations(candidates_to_min_distance)


def get_nodeID_by_coordinate(origin_coor, map):
    for key, value in map.stations.items():
        if value["x"] == origin_coor[0] and value["y"] == origin_coor[1]:
            return key

    return None


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

    origin_id = get_nodeID_by_coordinate(origin_coor, map)
    destination_id = get_nodeID_by_coordinate(dest_coor, map)
    cost_dictionary = {}

    if origin_id is None or destination_id is None:
        return Path(-1)

    list_of_path = [Path(origin_id)]

    while len(list_of_path) != 0 and destination_id not in list_of_path[0].route:
        first_element_list = list_of_path[0]
        expanded_path = expand(first_element_list, map)
        expanded_path = remove_cycles(expanded_path)

        expanded_path = calculate_cost(expanded_path, map, type_preference)
        expanded_path = calculate_heuristics(expanded_path, map, destination_id, type_preference)
        expanded_path = update_f(expanded_path)
        list_of_path = insert_cost_f(expanded_path, list_of_path)
        expanded_path, list_of_path, cost_dictionary = remove_redundant_paths(expanded_path, list_of_path, cost_dictionary)

    return list_of_path[0]
