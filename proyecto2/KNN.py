__authors__ = ['1499617','1456140','1456845']
__group__ = 'DM.18'

import numpy as np
import math
import operator
import json
from scipy.spatial.distance import cdist

class KNN:
    def __init__(self, train_data, labels):

        self._init_train(train_data)
        self.labels = np.array(labels)
        #############################################################
        ##  THIS FUNCTION CAN BE MODIFIED FROM THIS POINT, if needed
        #############################################################


    def _init_train(self,train_data):
        """
        initializes the train data
        :param train_data: PxMxNx3 matrix corresponding to P color images
        :return: assigns the train set to the matrix self.train_data shaped as PxD (P points in a D dimensional space)
        """
        if train_data.dtype != 'float':
            train_data = train_data.astype('float')

        second_dimension = 1
        for i in range(1, len(train_data.shape)):
            second_dimension = second_dimension * train_data.shape[i]

        self.train_data = train_data.reshape(train_data.shape[0], second_dimension)


    def get_k_neighbours(self, test_data, k):
        """
        given a test_data matrix calculates de k nearest neighbours at each point (row) of test_data on self.neighbors
        :param test_data:   array that has to be shaped to a NxD matrix ( N points in a D dimensional space)
        :param k:  the number of neighbors to look at
        :return: the matrix self.neighbors is created (NxK)
                 the ij-th entry is the j-th nearest train point to the i-th test point
        """
        second_dimension = 1
        for i in range(1, len(test_data.shape)):
            second_dimension = second_dimension * test_data.shape[i]

        test_data_to_use  = test_data.reshape(test_data.shape[0], second_dimension)
        distances_between_points = cdist(test_data_to_use, self.train_data)
        index_of_minimun = distances_between_points.argsort()
        index_of_minimun = index_of_minimun[0:, 0:k]
        arrayToConvert = []

        for i in range(index_of_minimun.shape[0]):
            helper = []
            for j in range(index_of_minimun.shape[1]):
                helper.append(self.labels[index_of_minimun[i][j]])
            arrayToConvert.append(helper)

        self.neighbors = np.array(arrayToConvert)


    def get_class(self):
        """
        Get the class by maximum voting
        :return: 2 numpy array of Nx1 elements.
                1st array For each of the rows in self.neighbors gets the most voted value
                            (i.e. the class at which that row belongs)
                2nd array For each of the rows in self.neighbors gets the % of votes for the winning class
        """
        #######################################################
        ##  YOU MUST REMOVE THE REST OF THE CODE OF THIS FUNCTION
        ##  AND CHANGE FOR YOUR OWN CODE
        #######################################################
        list_to_return_value = []
        value_counts = []

        for i in range(self.neighbors.shape[0]):
            unique,index,counts = np.unique(self.neighbors[i], return_counts=True, return_index=True)
            value_counts.append(counts)
            values_where_max_starts = np.where(counts == np.amax(counts))

            if values_where_max_starts[0].size == index.size:
                index_where_the_value_appears_firts_time = index.min()

            elif values_where_max_starts[0].size == 1:
                index_where_the_value_appears_firts_time = index[values_where_max_starts[0][0]]

            else:
                index_where_the_value_appears_firts_time = index[values_where_max_starts[0]].min()

            list_to_return_value.append(self.neighbors[i][index_where_the_value_appears_firts_time])

        return np.array(list_to_return_value)#, np.array(value_counts)


    def predict(self, test_data, k):
        """
        predicts the class at which each element in test_data belongs to
        :param test_data: array that has to be shaped to a NxD matrix ( N points in a D dimensional space)
        :param k:         :param k:  the number of neighbors to look at
        :return: the output form get_class (2 Nx1 vector, 1st the classm 2nd the  % of votes it got
        """
        self.get_k_neighbours(test_data,k)
        return self.get_class()
