import numpy as np

def get_max_delta(deltas):
    max_deltas = []
    deltas_count = len(deltas)     # Numero de deltas de distintos nodos
    layer_count = len(deltas[0])  # Numero de capas
    for layer_index in range(layer_count):
        layer_max_delta = deltas[0][layer_index]
        for node_index in range(1, deltas_count):
            layer_max_delta = np.maximum(layer_max_delta, deltas[node_index][layer_index])
        max_deltas.append(layer_max_delta)
    return max_deltas

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

max_delta = get_max_delta(deltas)

print(max_delta[0])
print(max_delta[1])
