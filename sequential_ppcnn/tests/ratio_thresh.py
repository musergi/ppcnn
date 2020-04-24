import numpy as np
import random

def get_ratio_thresh_delta(delta):
    ratio_thresh_deltas = []
    nodes = range(0, len(deltas))
    layers = range(0, len(deltas[0]))
    for layer in layers:
        layer_weights = list()
        layer_max_delta = deltas[0][layer]
        for node in nodes:
            layer_weights.append(deltas[node][layer])
            layer_max_delta = np.maximum(layer_max_delta, deltas[node][layer])
        #Define a random number between median and a 50% between median and maximun
        layer_median_delta = np.median(layer_weights, axis=0)
        layer_difference_delta = (layer_max_delta - layer_median_delta)/2
        ratio_thresh_deltas.append(random.uniform(layer_median_delta, layer_median_delta + layer_difference_delta))
    return ratio_thresh_deltas


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

    ratio_thresh = get_ratio_thresh_delta(deltas)
    print(ratio_thresh)