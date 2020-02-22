import tensorflow as tf 
import threading

class Controller(object):
    instance = None       
    def __new__(cls, *args, **kargs): 
        if cls.instance is None:
            cls.instance = object.__new__(cls, *args, **kargs)
        return cls.instance

    def create_network(self):
        self.network = NetworkMonitor()

    def to_json(self):
        return self.network.to_json()

    def get_weights(self):
        return self.network.get_weights()

    def set_weights(self, weights):
        self.network.set_weights(weights)

class NetworkMonitor:
    def __init__(self):
        self._lock = threading.Lock()
        self.model = tf.keras.Sequential([
            tf.keras.layers.Flatten(input_shape=(32, 32)),
            tf.keras.layers.Dense(1024, activation='relu'),
            tf.keras.layers.Dense(256, activation='relu'),
            tf.keras.layers.Dense(128, activation='relu'),
            tf.keras.layers.Dense(10, activation='softmax')
        ])
        self.model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    
    def to_json(self):
        json = None
        with self._lock:
            json = self.model.to_json()
        return json

    def get_weights(self):
        weights = None
        with self._lock:
            weights = self.model.get_weights()
        return weights

    def set_weights(self, weights):
        with self._lock:
            self.model.set_weights(weights)
        

def calculate_gradient(initial_weights, final_weights):
    delta = list()
    for initial_weight, final_weight in zip(initial_weights, final_weights):
        delta.append(final_weight - initial_weight)
    return delta


def apply_gradient(weights, gradients):
    result = list()
    for weight, gradient in zip(weights, gradients):
        result.append(weight + gradient)
    return result

#Save the dataset to a file
def save_to_file(filepath, model):
    model.save(filepath, save_format='h5')


def evaluate_dataset(model_path, validation_data):
    model = tf.keras.models.load_model(model_path)
    return model.evaluate(validation_data)


if __name__ == "__main__":
    import numpy as np
    initial = [np.array([1, 2, 3])]
    final = [np.array([1, 1, 1])]
    print(calculate_gradient(initial, final))