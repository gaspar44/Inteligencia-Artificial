from utils import *
from SearchAlgorithm import *
import os
if __name__ == '__main__':
    ROOT_FOLDER = '../CityInformation/Lyon_smallCity/'
    erMap = read_station_information(os.path.join(ROOT_FOLDER, 'Stations.txt'))
    connections = read_cost_table(os.path.join(ROOT_FOLDER, 'Time.txt'))
    erMap.add_connection(connections)
    erPath = depth_first_search(2, 7, erMap)
    print(erPath)
