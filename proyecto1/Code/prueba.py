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

    origin_id = [108, 206]
    destination_id = [67, 79]
    Astar(origin_id,destination_id,erMap,1)
