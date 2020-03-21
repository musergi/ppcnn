import numpy as np 
 
def get_geometric_mean_delta(deltas, nodes):
    gmean_deltas = []
        for layer in range(len(deltas[0])):
            gmean_layer_deltas = None
            for node_deltas in deltas:
                if gmean_layer_deltas is None:
                    gmean_layer_deltas = node_deltas[layer] / len(deltas)
                else:
                    gmean_layer_deltas = gmean_layer_deltas * (node_deltas[layer] / len(deltas))
            gmean_layer_deltas = np.sqrt(gmean_layer_deltas, order=nodes)
            gmean_deltas.append(gmean_layer_deltas)
    return gmean_deltas 
 
