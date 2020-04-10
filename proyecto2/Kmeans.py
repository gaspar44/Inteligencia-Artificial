__authors__ = ['1499617']
__group__ = 'DM.18'

from calendar import different_locale

import numpy as np
import utils

class KMeans:

    def __init__(self, X, K=1, options=None):
        """
         Constructor of KMeans class
             Args:
                 K (int): Number of cluster
                 options (dict): dictºionary with options
            """
        self.num_iter = 0
        self.K = K
        self._init_X(X)
        self._init_options(options)  # DICT options

    #############################################################
    ##  THIS FUNCTION CAN BE MODIFIED FROM THIS POINT, if needed
    #############################################################


    def _init_X(self, X):
        """Initialization of all pixels, sets X as an array of data in vector form (PxD)
            Args:
                X (list or np.array): list(matrix) of all pixel values
                    if matrix has more than 2 dimensions, the dimensionality of the smaple space is the length of
                    the last dimension
        """
        if X.dtype != 'float':
            X = X.astype('float')

            self.X = np.reshape(X, (-1, X.shape[-1])) if len(X.shape) >= 3 else X

    def _init_options(self, options=None):
        """
        Initialization of options in case some fields are left undefined
        Args:
            options (dict): dictionary with options
        """
        if options == None:
            options = {}
        if not 'km_init' in options:
            options['km_init'] = 'first'
        if not 'verbose' in options:
            options['verbose'] = False
        if not 'tolerance' in options:
            options['tolerance'] = 0
        if not 'max_iter' in options:
            options['max_iter'] = np.inf
        if not 'fitting' in options:
            options['fitting'] = 'WCD'  #within class distance.

        # If your methods need any other prameter you can add it to the options dictionary
        self.options = options

        #############################################################
        ##  THIS FUNCTION CAN BE MODIFIED FROM THIS POINT, if needed
        #############################################################


    def _init_centroids(self):
        """
        Initialization of centroids
        """
        if self.options['km_init'].lower() == 'first':
            self.K_point_ID = np.array(self.K)
            arrays_to_find = self.K - 1
            different_elements = self.X[0]
            different_elements_list = [self.X[0].tolist()]

            for i in range(1, self.X.shape[0]):
                mask = np.array_equal(different_elements, self.X[i])
                if not np.all(mask):
                    element_as_list = self.X[i].tolist()
                    if element_as_list not in different_elements_list:
                        different_elements_list.append(element_as_list)
                        different_elements = np.append(different_elements,self.X[i])
                        arrays_to_find = arrays_to_find - 1
                        if arrays_to_find <= 0:
                            self.centroids = different_elements.reshape(different_elements.shape[0]//self.X.shape[1], self.X.shape[1])
                            self.old_centroids = None
                            return
        else:
            self.centroids = np.random.rand(self.K, self.X.shape[1])
            self.old_centroids = np.random.rand(self.K, self.X.shape[1])


    def get_labels(self):
        """        Calculates the closest centroid of all points in X
        and assigns each point to the closest centroid
        """

        #######################################################
        ##  YOU MUST REMOVE THE REST OF THE CODE OF THIS FUNCTION
        ##  AND CHANGE FOR YOUR OWN CODE
        #######################################################
        self.distance_between_points = distance(self.X, self.centroids)
        self.labels = np.zeros(self.X.shape[0])
        for i in range(self.distance_between_points.shape[0]):
                min_distance = np.amin(self.distance_between_points[i])
                index_of_distance = np.where(self.  distance_between_points[i] == min_distance)
                self.labels[i] = index_of_distance[0][0]


    def get_centroids(self):
        """
        Calculates coordinates of centroids based on the coordinates of all the points assigned to the centroid
        """
        #######################################################
        ##  YOU MUST REMOVE THE REST OF THE CODE OF THIS FUNCTION
        ##  AND CHANGE FOR YOUR OWN CODE
        #######################################################
        unique = np.unique(self.labels)
        new_centroids = np.zeros( (self.centroids.shape[0], self.centroids.shape[1] ) )
        dict_of_count = dict.fromkeys(unique)

        for key in dict_of_count:
            dict_of_count[key] = []

        for i in range(self.X.shape[0]):
            key_to_use = int(self.labels[i])
            value_to_append = self.X[i]
            dict_of_count[key_to_use].append(value_to_append.tolist())

        for key in dict_of_count:
            dict_of_count[key] = np.array(dict_of_count[key])
            dict_of_count[key] = np.mean(dict_of_count[key], axis=0)
            new_centroids[int(key)] = dict_of_count[key]

        self.old_centroids = self.centroids
        self.centroids = new_centroids



    def converges(self):
        """
        Checks if there is a difference between current and old centroids
        """
        #######################################################
        ##  YOU MUST REMOVE THE REST OF THE CODE OF THIS FUNCTION
        ##  AND CHANGE FOR YOUR OWN CODE
        #######################################################
        return True

    def fit(self):
        """
        Runs K-Means algorithm until it converges or until the number
        of iterations is smaller than the maximum number of iterations.
        """
        #######################################################
        ##  YOU MUST REMOVE THE REST OF THE CODE OF THIS FUNCTION
        ##  AND CHANGE FOR YOUR OWN CODE
        #######################################################
        pass

    def whitinClassDistance(self):
        """
         returns the whithin class distance of the current clustering
        """

        #######################################################
        ##  YOU MUST REMOVE THE REST OF THE CODE OF THIS FUNCTION
        ##  AND CHANGE FOR YOUR OWN CODE
        #######################################################
        return np.random.rand()

    def find_bestK(self, max_K):
        """
         sets the best k anlysing the results up to 'max_K' clusters
        """
        #######################################################
        ##  YOU MUST REMOVE THE REST OF THE CODE OF THIS FUNCTION
        ##  AND CHANGE FOR YOUR OWN CODE
        #######################################################
        pass


def distance(X, C):
    """
    Calculates the distance between each pixcel and each centroid
    Args:
        X (numpy array): PxD 1st set of data points (usually data points)
        C (numpy array): KxD 2nd set of data points (usually cluster centroids points)

    Returns:
        dist: PxK numpy array position ij is the distance between the
        i-th point of the first set an the j-th point of the second set
    """

    #########################################################
    ##  YOU MUST REMOVE THE REST OF THE CODE OF THIS FUNCTION
    ##  AND CHANGE FOR YOUR OWN CODE
    #########################################################
    distances_to_return = []
    for i in range(X.shape[0]):
        distances_found = []
        for j in range(C.shape[0]):
            distance = np.linalg.norm(C[j]-X[i])
            distances_found.append(distance)
        distances_to_return.append(distances_found)

    return np.array(distances_to_return)


def get_colors(centroids):
    """
    for each row of the numpy matrix 'centroids' returns the color laber folllowing the 11 basic colors as a LIST
    Args:
        centroids (numpy array): KxD 1st set of data points (usually centroind points)

    Returns:
        lables: list of K labels corresponding to one of the 11 basic colors
    """

    #########################################################
    ##  YOU MUST REMOVE THE REST OF THE CODE OF THIS FUNCTION
    ##  AND CHANGE FOR YOUR OWN CODE
    #########################################################
    return list(utils.colors)
