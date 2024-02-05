from tensorflow import keras
import tensorflow as tf
import pathlib
import numpy as np

class Predictor:
    digit_recognizer = keras.models.load_model(pathlib.Path('Models', 'digit_recognizer.keras'))
    wall_recognizer = keras.models.load_model(pathlib.Path('Models', 'wall_recognizer.keras'))

    @staticmethod
    def format_image(image: np.ndarray) -> tf.data.Dataset:
        image = tf.data.Dataset.from_tensor_slices([image])
        def transform(x):
            x = tf.reshape(x, [1, 28, 28, 1])
            x = tf.cast(x, tf.float32) / 255
            x = tf.image.resize(x, [28,28])
            return x
        image = image.map(transform)
        return image

    @classmethod
    def detect_digit(cls, image: np.ndarray) -> int:
        image = cls.format_image(image)
        return cls.digit_recognizer.predict(image).argmax(axis=1)[0]

    @classmethod
    def detect_borders(cls, image: np.ndarray) -> tuple[bool, bool, bool, bool]:
        image = cls.format_image(image)
        return tuple((cls.wall_recognizer.predict(image) >= 0.5)[0])
    
