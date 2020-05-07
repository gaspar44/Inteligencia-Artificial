__authors__ = 'TO_BE_FILLED'
__group__ = 'TO_BE_FILLED'

import numpy as np
import Kmeans
import KNN
from utils_data import read_dataset, visualize_k_means, visualize_retrieval
import matplotlib.pyplot as plt
import time

# Analisis cuantitativo
def kmeans_statistics(images,KMax):
    times = []
    iterations = []
    wcds = []

    for i in range(2, KMax):
        km = Kmeans.KMeans(images, i)
        time1 = time.time()
        iterations_needed = km.fit()
        times.append(time.time() - time1)
        iterations.append(iterations_needed)
        wcds.append(km.whitinClassDistance())

    return times, iterations, wcds


if __name__ == '__main__':

    #Load all the images and GT
    train_imgs, train_class_labels, train_color_labels, \
    test_imgs, test_class_labels, test_color_labels = read_dataset(ROOT_FOLDER='./images/', gt_json='./images/gt.json')

    #List with all the existant classes
    classes = list(set(list(train_class_labels) + list(test_class_labels)))


    K_MAX = 11
    for i in range(1):
        times, iterations, WCD = kmeans_statistics(train_imgs[0], K_MAX)
        # plt.scatter([2, 3, 4, 5, 6, 7, 8, 9, 10], prueba1)
        # plt.xlabel("K")
        # plt.ylabel("time")
        # plt.show()
        plt.scatter(list(range(2, K_MAX)), WCD)
        plt.xlabel("K")
        plt.ylabel("WCD")
        #plt.show()
        plt.savefig("wcd.png")

## You can start coding your functions here