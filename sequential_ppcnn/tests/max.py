import numpy as np

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
