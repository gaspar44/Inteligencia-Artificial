__authors__ = 'TO_BE_FILLED'
__group__ = 'TO_BE_FILLED'

import numpy as np
import Kmeans
import KNN
from utils_data import read_dataset, visualize_k_means, visualize_retrieval,Plot3DCloud
import matplotlib.pyplot as plt
import time
import random
import os

output_folder = "./resultados/"
# Analisis cuantitativo
def get_statistics(train_imgs,number_of_images_to_use):
    plt.clf()
    K_MAX = 11
    times_to_graph = []
    iterations_to_graph = []
    WCDs_to_graph = []
    print("calculating kmeans for: ", number_of_images_to_use)

    time1 = time.time()
    ## Default kmeans time: 28 segs
    for i in range(number_of_images_to_use):
        numberToUse = random.randint(0, train_imgs.shape[0])
        times, iterations, WCD = kmeans_statistics(train_imgs[numberToUse], K_MAX)
        times_to_graph.append(times)
        iterations_to_graph.append(iterations)
        WCDs_to_graph.append(WCD)

    for i in range(number_of_images_to_use):
        plt.scatter(list(range(2, K_MAX)), iterations_to_graph[i])
        plt.title("iterations")
        plt.xlabel("K")
        plt.ylabel("iterations")
        plt.savefig(output_folder + "iterations.png")

    plt.clf()

    for i in range(number_of_images_to_use):
        plt.scatter(list(range(2, K_MAX)), WCDs_to_graph[i])
        plt.xlabel("K")
        plt.ylabel("WCD")
        plt.savefig(output_folder + "wcd.png")

    plt.clf()

    for i in range(number_of_images_to_use):
        plt.scatter(list(range(2, K_MAX)), times_to_graph[i])
        plt.xlabel("K")
        plt.ylabel("time(seg)")
        plt.savefig(output_folder + "time.png")

    print(time - time1)


def get_shape_accuracy(knn_labels,test_labels):
    equals = np.char.equal(knn_labels, test_labels)
    _, counts = np.unique(equals,return_counts=True)
    return (counts[1]/knn_labels.shape[0]) * 100


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


def get_knn_accuracy_(train_imgs, train_class_labels,K_max):
    plt.clf()
    knn = KNN.KNN(train_imgs, train_class_labels)
    distances_to_use = ["euclidean", "cityblock", "cosine", "seuclidean"]
    print("starting knn with next heuristics for distance: " ,distances_to_use)
    print("estimated time 12 mins")

    for distance in distances_to_use:
        time.sleep(3)
        percentags_returned = []
        time1 = time.time()

        for i in range(2, K_max):
            labels = knn.predict(test_imgs, i, distance)
            asserted_label_percentaje = get_shape_accuracy(labels, test_class_labels)
            percentags_returned.append(asserted_label_percentaje)

        print(distance + " finished in: ", time.time() - time1)

        #Graph
        plt.clf()
        plt.scatter(list(range(2, K_max)), percentags_returned)
        plt.title("KNN % " + distance + " success")
        plt.xlabel("K")
        plt.ylabel("%")
        plt.savefig(output_folder + "porcentaje" + distance + ".png")


if __name__ == '__main__':
    print("WARNING: the will be Kmeans and knn calculated from 2 to 11. KMeans will take 30 random pictures to analyze and knn all. This means it will take time.\n")
    print("The estimated time will be outputed at the start of every function. The PID will be output for kill reasons.\n")
    agreedment = input("if you are ok with this: type 'yes' ")

    if str(agreedment).lower() != "yes":
        exit(0)
    #Load all the images and GT
    train_imgs, train_class_labels, train_color_labels, \
    test_imgs, test_class_labels, test_color_labels = read_dataset(ROOT_FOLDER='./images/', gt_json='./images/gt.json')

    #List with all the existant classes
    classes = list(set(list(train_class_labels) + list(test_class_labels)))
    print("process PID: ", os.getpid())
    print("KMax for every algorithm: ", 11)

    if not os.path.exists(output_folder):
        print("folder " + output_folder + " created for output")
        os.mkdir(output_folder)

    get_statistics(train_imgs, 10)
    get_knn_accuracy_(train_imgs, train_class_labels, 11)

## You can start coding your functions here