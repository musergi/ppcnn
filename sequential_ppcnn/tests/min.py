import numpy as np

def get_min_delta(deltas):
    min_deltas = []
    deltas_count = len(deltas)     # Numero de deltas de distintos nodos
    layer_count = len(deltas[0])  # Numero de capas
    for layer_index in range(layer_count):
        layer_min_delta = deltas[0][layer_index]
        for node_index in range(1, deltas_count):
            layer_min_delta = np.minimum(layer_min_delta, deltas[node_index][layer_index])
        min_deltas.append(layer_min_delta)
    return min_deltas

deltas_node1 = [
    np.array([[1, 1, 1], [1, 2, 1]]), # Layer 1
    np.array([[2, 2, 2], [2, 7, 2]])  # Layer 2
]
deltas_node2 = [
    np.array([[3, 4, 2], [2, 2, 3]]), # Layer 1
    np.array([[2, 2, 2], [2, 4, 2]])  # Layer 2
]
deltas_node3 = [
    np.array([[4, 2, 1], [3, 2, 1]]), # Layer 1
    np.array([[5, 2, 2], [3, 7, 2]])  # Layer 2
]
deltas = [deltas_node1, deltas_node2, deltas_node3]

min_delta = get_min_delta(deltas)

print(min_delta[0])
print(min_delta[1])