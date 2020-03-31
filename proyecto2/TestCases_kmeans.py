import unittest
import pickle
import Kmeans as km
import numpy as np
from Kmeans import *
from utils import *


class TestCases(unittest.TestCase):


    def setUp(self):
        np.random.seed(123)
        with open('./test/test_cases_kmeans.pkl', 'rb') as f:
            self.test_cases = pickle.load(f)

    def test_NIU(self):
        # DON'T FORGET TO WRITE YOUR NIU AND GROUPS
        self.assertNotEqual(km.__authors__, "TO_BE_FILLED", msg="CHANGE IT TO YOUR NIU!")
        self.assertNotEqual(km.__group__, "TO_BE_FILLED", msg="CHANGE YOUR GROUP NAME!")

    def test_init_X(self):
        for ix, input in enumerate(self.test_cases['input']):
            km = KMeans(input, self.test_cases['K'][ix])
            np.testing.assert_array_equal(km.X, self.test_cases['shape'][ix])

    def test_init_centroids(self):
        for ix, input in enumerate(self.test_cases['input']):
            km = KMeans(input, self.test_cases['K'][ix])
            km._init_centroids()
            np.testing.assert_array_equal(km.centroids, self.test_cases['init_centroid'][ix])

    def test_distance(self):
        for ix, input in enumerate(self.test_cases['shape']):
            dist = distance(input, self.test_cases['init_centroid'][ix])
            np.testing.assert_array_equal(dist, self.test_cases['distance'][ix])

    def test_get_labels(self):
        for ix, input in enumerate(self.test_cases['input']):
            km = KMeans(input, self.test_cases['K'][ix])
            km._init_centroids()
            km.get_labels()
            np.testing.assert_array_equal(km.labels, self.test_cases['labels'][ix])

    def test_get_centroids(self):
        for ix, input in enumerate(self.test_cases['input']):
            km = KMeans(input, self.test_cases['K'][ix])
            km._init_centroids()
            km.get_labels()
            km.get_centroids()
            # Compare old centroids
            np.testing.assert_array_equal(km.old_centroids, self.test_cases['get_centroid'][ix][0])
            # Compare new centroids
            np.testing.assert_array_equal(km.centroids, self.test_cases['get_centroid'][ix][1])

    def test_converges(self):
        for ix, input in enumerate(self.test_cases['input']):
            km = KMeans(input, self.test_cases['K'][ix])
            km._init_centroids()
            old_centroid, centroid, bool_value = self.test_cases['converge'][ix]
            km.old_centroids, km.centroids = old_centroid, centroid
            self.assertEqual(km.converges(), bool_value)

    def test_Kmeans(self):
        for ix, input in enumerate(self.test_cases['input']):
            km = KMeans(input, self.test_cases['K'][ix])
            km.fit()
            np.testing.assert_array_equal(km.centroids, self.test_cases['kmeans'][ix])


    def test_find_bestK(self):
        for ix, input in enumerate(self.test_cases['input']):
            km = KMeans(input, self.test_cases['K'][ix])
            km.find_bestK(10)
            self.assertEqual(km.K, self.test_cases['bestK'][ix])



    def test_get_color(self):
        for ix, centroid in enumerate(self.test_cases['kmeans']):
            color = get_colors(centroid)
            self.assertCountEqual(color, self.test_cases['color'][ix])


if __name__ == "__main__":
    unittest.main()
