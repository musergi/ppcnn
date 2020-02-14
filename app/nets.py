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

    


if __name__ == "__main__":
    c = Controller()
    c.create_network()
    c.get_weights()