import unittest
from SearchAlgorithm import *
from SubwayMap import *
from utils import *
import os
import random


class TestCases(unittest.TestCase):
    ROOT_FOLDER = '../CityInformation/Lyon_smallCity/'

    def setUp(self):
        map = read_station_information(os.path.join(self.ROOT_FOLDER, 'Stations.txt'))
        connections = read_cost_table(os.path.join(self.ROOT_FOLDER, 'Time.txt'))
        map.add_connection(connections)

        infoVelocity_clean = read_information(os.path.join(self.ROOT_FOLDER, 'InfoVelocity.txt'))
        map.add_velocity(infoVelocity_clean)

        self.map = map

    def test_Expand(self):
        expanded_paths = expand(Path(7), self.map)
        self.assertEqual(expanded_paths, [Path([7, 6]), Path([7, 8])])

        expanded_paths = expand(Path([13, 12]), self.map)
        self.assertEqual(expanded_paths, [Path([13, 12, 8]), Path([13, 12, 11]), Path([13, 12, 13])])

        expanded_paths = expand(Path([14, 13, 8, 12]), self.map)
        self.assertEqual(expanded_paths, [Path([14, 13, 8, 12, 8]),
                                          Path([14, 13, 8, 12, 11]),
                                          Path([14, 13, 8, 12, 13])])

    def test_RemoveCycles(self):
        expanded_paths = expand(Path(7), self.map)
        expanded_paths = remove_cycles(expanded_paths)
        self.assertEqual(expanded_paths, [Path([7, 6]), Path([7, 8])])

        expanded_paths = expand(Path([13, 12]), self.map)
        expanded_paths = remove_cycles(expanded_paths)
        self.assertEqual(expanded_paths, [Path([13, 12, 8]), Path([13, 12, 11])])

        expanded_paths = expand(Path([14, 13, 8, 12]), self.map)
        expanded_paths = remove_cycles(expanded_paths)
        self.assertEqual(expanded_paths, [Path([14, 13, 8, 12, 11])])

    def test_depth_first_search(self):
        route1 = depth_first_search(2, 7, self.map)
        route2 = depth_first_search(13, 1, self.map)
        route3 = depth_first_search(5, 12, self.map)
        route4 = depth_first_search(14, 10, self.map)

        self.assertEqual(route1, Path([2, 5, 6, 7]))
        self.assertEqual(route2, Path([13, 8, 7, 6, 5, 2, 1]))
        self.assertEqual(route3, Path([5, 2, 10, 11, 12]))
        self.assertEqual(route4, Path([14, 13, 8, 7, 6, 5, 2, 10]))

    def test_breadth_first_search(self):
        route1 = breadth_first_search(2, 7, self.map)
        route2 = breadth_first_search(13, 1, self.map)
        route3 = breadth_first_search(5, 12, self.map)
        route4 = breadth_first_search(14, 10, self.map)

        self.assertEqual(route1, Path([2, 5, 6, 7]))
        self.assertEqual(route2, Path([13, 12, 11, 10, 2, 1]))
        self.assertEqual(route3, Path([5, 10, 11, 12]))
        self.assertEqual(route4, Path([14, 13, 12, 11, 10]))

    def test_calculate_cost(self):
        list_of_path = [Path([7, 6]), Path([7, 8])]
        updated_paths = calculate_cost(list_of_path, self.map, type_preference=0)
        self.assertEqual([path.g for path in updated_paths], [1, 1])

        list_of_path = [Path([7, 6]), Path([7, 8])]
        updated_paths = calculate_cost(list_of_path, self.map, type_preference=1)
        self.assertEqual([path.g for path in updated_paths], [4.21429, 6.03739])

        list_of_path = [Path([7, 6]), Path([7, 8])]
        updated_paths = calculate_cost(list_of_path, self.map, type_preference=2)
        self.assertEqual([path.g for path in updated_paths], [59.000060000000005, 84.52346])

        list_of_path = [Path([7, 6]), Path([7, 8])]
        updated_paths = calculate_cost(list_of_path, self.map, type_preference=3)
        self.assertEqual([path.g for path in updated_paths], [0, 0])

    def test_uniform_cost_search(self):
        route = uniform_cost_search(9, 3, self.map, 0)
        self.assertEqual(route, Path([9, 8, 7, 6, 5, 2, 3]))

        route = uniform_cost_search(9, 3, self.map, 1)
        self.assertEqual(route, Path([9, 8, 12, 11, 10, 2, 3]))

        route = uniform_cost_search(9, 3, self.map, 2)
        self.assertEqual(route, Path([9, 8, 12, 11, 10, 2, 3]))

        route = uniform_cost_search(9, 3, self.map, 3)
        self.assertEqual(route, Path([9, 8, 7, 6, 5, 2, 3]))

    def test_calculate_heuristics(self):
        expanded_paths = [Path([12, 8, 7]), Path([12, 8, 9]), Path([12, 8, 13])]
        updated_paths = calculate_heuristics(expanded_paths, self.map, destination_id=9, type_preference=0)
        self.assertEqual([path.h for path in updated_paths], [1, 0, 1])

        expanded_paths = [Path([12, 8, 7]), Path([12, 8, 9]), Path([12, 8, 13])]
        updated_paths = calculate_heuristics(expanded_paths, self.map, destination_id=9, type_preference=1)
        self.assertEqual([path.h for path in updated_paths], [1.8544574262244504, 0.0, 0.6273597428219158])

        expanded_paths = [Path([12, 8, 7]), Path([12, 8, 9]), Path([12, 8, 13])]
        updated_paths = calculate_heuristics(expanded_paths, self.map, destination_id=9, type_preference=2)
        self.assertEqual([path.h for path in updated_paths], [83.45058418010026, 0.0, 28.231188426986208])

        expanded_paths = [Path([12, 8, 7]), Path([12, 8, 9]), Path([12, 8, 13])]
        updated_paths = calculate_heuristics(expanded_paths, self.map, destination_id=9, type_preference=3)
        self.assertEqual([path.h for path in updated_paths], [0, 0, 1])

    def create_path_with_g(self, r, g):
        path = Path(r)
        path.g = g
        return path

    def print_paths(self, new_paths, list_of_path_removed):
        print('New expanded paths:')
        print_list_of_path_with_cost(new_paths)
        print('List of paths:')
        print_list_of_path_with_cost(list_of_path_removed)

    def test_remove_redundant_path(self):
        # Necessary setup for testing
        path_1 = self.create_path_with_g([12, 8, 7], 84.52)
        path_2 = self.create_path_with_g([12, 8, 13, 9], 235.23)
        path_3 = self.create_path_with_g([12, 8, 15, 11], 350.12)
        # these are the paths you have to check
        list_of_path = [path_1, path_2, path_3]
        # this the expanded path of path_1
        expand_paths = [self.create_path_with_g([12, 8, 7, 11], 124.52), self.create_path_with_g([12, 8, 7, 15], 222.52)]
        # Now imagine you have the cost dictionary
        cost_dict = {13: 0, 7: 169.04692, 9: 235.23, 15: 400, 11: 350.12}
        new_paths, list_of_path_removed, _ = remove_redundant_paths(expand_paths, list_of_path, cost_dict)
        # If you would like to print the paths uncomment the line below
        self.print_paths(new_paths, list_of_path_removed)
        self.assertEqual(list_of_path_removed, [path_1, path_2])
        self.assertEqual(new_paths, expand_paths)

        cost_dict = {11: 350.12, 13: 0, 7: 84.52, 9: 235.23, 15: 200.10}
        expand_paths = [self.create_path_with_g([12, 8, 7, 11], 124.52),
                        self.create_path_with_g([12, 8, 7, 15], 222.52)]
        new_paths, list_of_path_removed, _ = remove_redundant_paths(expand_paths, list_of_path, cost_dict)
        # self.print_paths(new_paths, list_of_path_removed)
        self.assertEqual(list_of_path_removed, [path_1, path_2])
        self.assertEqual(new_paths, expand_paths[0:1])

    def test_coord2station(self):
        stationID = coord2station([105, 205], self.map)
        self.assertEqual(stationID, [8, 12, 13])

        stationID = coord2station([300, 111], self.map)
        self.assertEqual(stationID, [3])

        stationID = coord2station([10, 11], self.map)
        self.assertEqual(stationID, [1])

    def test_Astar(self):

        # If you want to see the optimal_path's route and f-cost,
        # uncomment the print functions below
        optimal_path = Astar([108, 206], [67, 79], self.map, 0)
        # print(optimal_path.route, optimal_path.f)
        self.assertEqual(optimal_path, Path([8, 7, 6, 5, 2, 1]))
        self.assertEqual(optimal_path.f, 5)

        optimal_path = Astar([140, 56], [140, 115], self.map, 1)
        # print(optimal_path.route, optimal_path.f)
        self.assertEqual(optimal_path, Path([2, 5, 6]))
        self.assertEqual(optimal_path.f, 27.14286)

        optimal_path = Astar([82, 217], [140, 27], self.map, 2)
        # print(optimal_path.route, optimal_path.f)
        self.assertEqual(optimal_path, Path([9, 8, 12, 11, 10, 5, 4]))
        self.assertEqual(optimal_path.f, 326.53992)

        optimal_path = Astar([167, 64], [152, 230], self.map, 3)
        # print(optimal_path.route, optimal_path.f)
        self.assertEqual(optimal_path, Path([3, 2, 10, 11, 12, 13, 14]))
        self.assertEqual(optimal_path.f, 2)


if __name__ == "__main__":
    unittest.main()