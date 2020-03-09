from utils import *
from SearchAlgorithm import *
import os
if __name__ == '__main__':
    ROOT_FOLDER = '../CityInformation/Lyon_smallCity/'
    erMap = read_station_information(os.path.join(ROOT_FOLDER, 'Stations.txt'))
    connections = read_cost_table(os.path.join(ROOT_FOLDER, 'Time.txt'))
    erMap.add_connection(connections)

    infoVelocity_clean = read_information(os.path.join(ROOT_FOLDER, 'InfoVelocity.txt'))
    erMap.add_velocity(infoVelocity_clean)

    erPath = depth_first_search(2, 7, erMap)
    list_of_path = [Path([12, 8, 3])]
    expanded_path = calculate_cost(list_of_path, erMap, 3)
    print(expanded_path[0].g)
