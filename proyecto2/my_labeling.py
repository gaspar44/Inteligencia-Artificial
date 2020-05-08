__authors__ = 'TO_BE_FILLED'
__group__ = 'TO_BE_FILLED'

import numpy as np
import Kmeans
import KNN
from utils_data import read_dataset, visualize_k_means, visualize_retrieval,Plot3DCloud
import matplotlib.pyplot as plt
import time
import random

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
    times_to_graph = []
    iterations_to_graph = []
    WCDs_to_graph = []
    ## Default kmeans time: 28 segs
    for i in range(10):
        numberToUse = random.randint(0, train_imgs.shape[0])
        times, iterations, WCD = kmeans_statistics(train_imgs[numberToUse], K_MAX)
        times_to_graph.append(times)
        iterations_to_graph.append(iterations)
        WCDs_to_graph.append(WCD)

    for i in range(10):
        plt.scatter(times_to_graph[i], iterations_to_graph[i])
        plt.legend()
        plt.title("iterations VS time")
        plt.xlabel("time/seg)")
        plt.ylabel("iterations")
        plt.savefig("iterations.png")

    plt.clf()

    for i in range(10):
        plt.scatter(list(range(2, K_MAX)), WCDs_to_graph[i])
        plt.xlabel("K")
        plt.ylabel("WCD")
        plt.savefig("wcd.png")

## You can start coding your functions here