import numpy as np

def get_median_delta(deltas):
    median_deltas = []
    deltas_count = len(deltas)     # Numero de deltas de distintos nodos
    layer_count = len(deltas[0])  # Numero de capas
    deltas = np.array(deltas)   # Convert the array into a numpy array
    for layer_index in range(layer_count):
        for node_index in range(1, deltas_count):
            layer_median_delta = np.median(deltas[node_index][layer_index], axis=node_index)
        median_deltas.append(layer_median_delta)
    return median_deltas

deltas_node1 = [
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

median_delta = get_median_delta(deltas)

print(median_delta[0])
print(median_delta[1])
