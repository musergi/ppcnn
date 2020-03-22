import numpy as np 
 
def get_geometric_mean_delta(deltas, nodes):
    gmean_deltas = []
    for layer in range(len(deltas[0])):
        gmean_layer_deltas = None
        for node_deltas in deltas:
            #Si hay un cero despreciarlo e decrementar nodes
            if gmean_layer_deltas is None:
                gmean_layer_deltas = node_deltas[layer] / len(deltas)
            else:
                gmean_layer_deltas = gmean_layer_deltas * (node_deltas[layer] / len(deltas))
        gmean_layer_deltas = np.sqrt(gmean_layer_deltas, order=nodes)
        gmean_deltas.append(gmean_layer_deltas)
    return gmean_deltas 


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

geometric_mean_delta = get_geometric_mean_delta(deltas, 3)

print(geometric_mean_delta[0])
print(geometric_mean_delta[1])

 
