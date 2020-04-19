import numpy as np
import random

def get_median(deltas):
    median_deltas = []
    nodes = range(0, len(deltas))
    layers = range(0, len(deltas[0]))
    for layer in layers:
        layer_weights = list()
        for node in nodes:
            layer_weights.append(deltas[node][layer])
        median_deltas.append(np.median(layer_weights, axis=0))
    return median_deltas

def get_max_delta(deltas):
    max_deltas = []
    nodes = range(0, len(deltas))
    layers = range(0, len(deltas[0]))
    for layer in layers:
        layer_max_delta = deltas[0][layer]
        for node in nodes:
            layer_max_delta = np.maximum(layer_max_delta, deltas[node][layer])
        max_deltas.append(layer_max_delta)
    return max_deltas

def get_thresh_delta(delta):
    median_deltas = []
    max_deltas = []
    thresh_deltas = []
    nodes = range(0, len(deltas))
    layers = range(0, len(deltas[0]))
    for layer in layers:
        layer_weights = list()
        layer_max_delta = deltas[0][layer]
        for node in nodes:
            layer_weights.append(deltas[node][layer])
            layer_max_delta = np.maximum(layer_max_delta, deltas[node][layer])
        thresh_deltas.append(random.uniform(np.median(layer_weights, axis=0), layer_max_delta))
    return thresh_deltas


if __name__ == '__main__':
    node1 = [
        np.array([[1, 1, 1], [1, 1, 1]]), # Layer 1 weights
        np.array([1, 1, 1])]              # Layer 1 biases
    
    node2 = [
        np.array([[2, 2, 2], [2, 2, 2]]), # Layer 1 weights
        np.array([2, 2, 2])]              # Layer 1 biases
    
    node3 = [
        np.array([[4, 4, 4], [4, 4, 4]]), # Layer 1 weights
        np.array([4, 4, 4])]              # Layer 1 biases
    deltas = [node1, node2, node3]
    median = get_median(deltas)
    maximum = get_max_delta(deltas)
    thresh = get_thresh_delta(deltas)
    print(thresh)