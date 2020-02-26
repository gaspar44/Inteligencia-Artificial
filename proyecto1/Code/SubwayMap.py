__authors__='TO_BE_FILLED'
__group__='TO_BE_FILLED'
# _________________________________________________________________________________________
# Intel.ligencia Artificial
# Grau en Enginyeria Informatica
# Curs 2016- 2017
# Universitat Autonoma de Barcelona
# _________________________________________________________________________________________

class Map:
    """
    A class for keeping all the data regarding stations and their connections

    self.stations: is a dictionary of dictionary with the format of
            {station_id: {"name": name_value, "line": line_value, ...}

    self.connectipns: is a dictionary of dictionary holding all the connection information with the format of
            {
                station_1 : {first_connection_to_station_1: cost_1_1, second_connection_to_station_1: cost_1_2}
                station_2 : {first_connection_to_station_2: cost_2_1, second_connection_to_station_1: cost_2_2}
                ....
            }
    """
    def __init__(self):
        self.stations = {}
        self.connections = {}

    def add_station(self, id, name, line, x, y):
        self.stations[id] = {'name': name, 'line': int(line), 'x': x, 'y': y}

    def add_connection(self, connections):
        self.connections = connections

    def combine_dicts(self):
        for k, v in self.stations.items():
            v.update({'velocity': self.velocity[v['line']]})

    def add_velocity(self, velocity):
        self.velocity = {ix+1: v for ix, v in enumerate(velocity)}
        self.combine_dicts()


class Path:
    """
    A class for keeping the route information from starting station to expanded station.
    Usage:
        # path is initialized with starting station number 2
        >>> path = Path(2)
        # Station 5 is added to the self.route
        >>> path.add_route(5)
        # Assume the cost from station 2 to station 5 is 10, we updated the path's cost
        >>> path.update_g(10)
        # You can reach the last and penultimate station of a path
        >>> path.last, path.penultimate
    """
    def __init__(self, route):
        if type(route) is list:
            self.route = route
        else:
            self.route = [route]

        self.head = self.route[0]
        self.last = self.route[-1]
        if len(self.route) >= 2: self.penultimate = self.route[-2]
        # Real cost
        self.g = 0
        # Heuristic cost
        self.h = 0
        # Combination of the two
        self.f = 0

    def __eq__(self, other):
        if other is not None:
            return self.route == other.route

    def update_h(self, h):
        self.h = h

    def update_g(self, g):
        self.g += g

    def update_f(self):
        self.f = self.g + self.h

    def add_route(self, children):
        # Adding a new station to the route list
        self.route.append(children)
        self.penultimate = self.route[-2]
        self.last = self.route[-1]
