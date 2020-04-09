import numpy as np


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
    print(get_median(deltas))


"""deltas_node1 = [
    np.array([[1, 1, 1], [1, 2, 1]]), # Layer 1
    np.array([[2, 2, 2], [2, 7, 2]])  # Layer 2
]
deltas_node2 = [
    np.array([[1, 4, 2], [1, 2, 3]]), # Layer 1
    np.array([[2, 2, 2], [2, 4, 2]])  # Layer 2
]
deltas_node3 = [
    np.array([[4, 2, 1], [3, 2, 1]]), # Layer 1
    np.array([[5, 2, 2], [3, 7, 2]])  # Layer 2
]
deltas = [deltas_node1, deltas_node2, deltas_node3]

median_delta = get_median_delta(deltas)"""

