import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, Flatten, MaxPooling2D, Dropout
import numpy as np
import matplotlib.pyplot as plt


class GeneticAlgo:
    def __init__(self, input_layer_shape, input_layer_neurons, number_of_hidden_layers, hidden_layer_neurons,
                 output_layer_shape, output_layer_neurons, inner_layer_activation, outer_layer_activation,
                 ):
        self.input_layer_shape = input_layer_shape
        self.input_layer_neurons = input_layer_neurons
        self.number_of_hidden_layers = number_of_hidden_layers
        self.hidden_layer_neurons = hidden_layer_neurons
        self.output_layer_shape = output_layer_shape
        self.output_layer_neurons = output_layer_neurons
        self.inner_layer_activation = inner_layer_activation
        self.outer_layer_activation = outer_layer_activation

    def nn_creation(self):
        pass

    def crossing(self):
        pass

    def mutation(self):
        pass


class NeuralNet:
    def __init__(self, input_layer_shape, input_layer_neurons, number_of_hidden_layers, hidden_layer_neurons,
                 output_layer_shape, output_layer_neurons, inner_layer_activation, outer_layer_activation):
        self.input_layer_shape = input_layer_shape
        self.input_layer_neurons = input_layer_neurons
        self.number_of_hidden_layers = number_of_hidden_layers
        self.hidden_layer_neurons = hidden_layer_neurons
        self.output_layer_shape = output_layer_shape
        self.output_layer_neurons = output_layer_neurons
        self.inner_layer_activation = inner_layer_activation
        self.outer_layer_activation = outer_layer_activation
        self.model = self.create_model()
        self.weights = self.model.get_weights()[0]

    def create_model(self):
        neural = Sequential()
        neural.add(Dense(self.input_layer_neurons, activation=self.inner_layer_activation,
                         input_shape=self.input_layer_shape))
        for i in range(0, self.number_of_hidden_layers):
            neural.add(Dense(self.hidden_layer_neurons[i], activation=self.inner_layer_activation))

        neural.add(Dense(self.output_layer_neurons, activation=self.outer_layer_activation))

        return neural
