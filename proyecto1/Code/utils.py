from SubwayMap import *
import numpy as np
import math
import signal
import time

# Infinite cost represented by INF
INF = 9999

def euclidean_dist(x, y):
    x1, y1 = x
    x2, y2 = y
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)

# readStationInformation: Given a filename, it reads the information of this file.
def read_station_information(filename):
    map = Map()
    with open(filename, 'r') as fileMetro:
        for line in fileMetro:
            information = line.split('\t')
            # TODO: Change the monstrous way of parsing
            map.add_station(int(information[0]), information[1], information[2], int(information[3]),
                                   int((information[4].replace('\n', '')).replace(' ', '')))
    return map


def read_information(filename):
    with open(filename, 'r') as fp:
        vel = fp.readlines()
        vel = [i.split('\n')[0] for i in vel]
    vector = [int(v.split(':')[-1]) for v in vel]
    return (vector)


def read_cost_table(filename):
    adj_matrix = np.loadtxt(filename)
    row, col = adj_matrix.nonzero()
    connections = {}
    for r, c in zip(row, col):
        if r+1 not in connections:
            connections[r + 1] = {c + 1: adj_matrix[r][c]}
        else:
            connections[r + 1].update({c + 1: adj_matrix[r][c]})

    return connections


def print_list_of_path(pathList):
    for p in pathList:
        print("Route: {}".format(p.route))


def print_list_of_path_with_cost(pathList):
    for p in pathList:
        print("Route: {}, \t Cost: {}".format(p.route, p.g))


class TestTimeout(Exception):
    pass

class test_timeout:
  def __init__(self, seconds, error_message=None):
    if error_message is None:
      error_message = 'test timed out after {}s.'.format(seconds)
    self.seconds = seconds
    self.error_message = error_message

  def handle_timeout(self, signum, frame):
    raise TestTimeout(self.error_message)

  def __enter__(self):
    signal.signal(signal.SIGALRM, self.handle_timeout)
    signal.alarm(self.seconds)

  def __exit__(self, exc_type, exc_val, exc_tb):
    signal.alarm(0)
