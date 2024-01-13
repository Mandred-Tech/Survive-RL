import random
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, Flatten, Dropout
import numpy as np
import pandas as pd
from base_envi import Simulation


class GeneticAlgo:
    def __init__(self, input_layer_shape, input_layer_neurons, number_of_hidden_layers, hidden_layer_neurons,
                 output_layer_neurons, inner_layer_activation, outer_layer_activation):
        # Initialization of genetic algorithm parameters and neural network model
        self.input_layer_shape = input_layer_shape
        self.input_layer_neurons = input_layer_neurons
        self.number_of_hidden_layers = number_of_hidden_layers
        self.hidden_layer_neurons = hidden_layer_neurons
        self.output_layer_neurons = output_layer_neurons
        self.inner_layer_activation = inner_layer_activation
        self.outer_layer_activation = outer_layer_activation
        self.model = self.create_model()  # Create initial neural network
        self.weights = self.model.layers[0].get_weights()[0]  # Get initial weights
        self.bias = self.model.layers[0].get_weights()[1]  # Get initial biases

    def nn_creation(self, number_of_nn):
        # Generate a list of neural networks with random initial weights
        neural_list = []
        for i in range(0, number_of_nn):
            model = self.create_model()
            neural_list.append(model)
        return neural_list

    def crossing(self, parent_nn1, parent_nn2, number_of_mutations):
        # Perform crossover between two parent neural networks to create a child network
        parent_nn1_weights = parent_nn1.get_weights()[0]
        parent_nn2_weights = parent_nn2.get_weights()[0]
        child_nn_weights = parent_nn1_weights
        child_nn_weights[random.randint(0, len(parent_nn1_weights) - 1)] = parent_nn2_weights[
            random.randint(0, len(parent_nn2_weights) - 1)]
        child_nn_weights = self.mutation(child_nn_weights, number_of_mutations)
        return child_nn_weights

    def mutation(self, nn_weights_to_mutate, number_of_mutations):
        # Introduce mutations to the weights of a neural network
        max_weight = np.max(nn_weights_to_mutate)
        min_weight = np.min(nn_weights_to_mutate)
        len_weights = len(nn_weights_to_mutate)
        each_list_len = len(nn_weights_to_mutate[0])
        for i in range(0, number_of_mutations):
            nn_weights_to_mutate[random.randint(0, len_weights - 1)][
                random.randint(0, each_list_len - 1)] = random.uniform(
                min_weight, max_weight)
        return nn_weights_to_mutate

    def create_model(self):
        # Create a neural network model using Keras Sequential API
        neural = Sequential()
        neural.add(Dense(self.input_layer_neurons, activation=self.inner_layer_activation,
                         input_shape=self.input_layer_shape))
        for i in range(0, self.number_of_hidden_layers):
            neural.add(Dense(self.hidden_layer_neurons[i], activation=self.inner_layer_activation))

        neural.add(Dense(self.output_layer_neurons, activation=self.outer_layer_activation))
        neural.compile(optimizer='adam', loss=None, metrics=None)
        return neural

    def create_offsprings(self, offspring_weights, number_of_offsprings):
        # Create a list of offspring neural networks with the given weights
        offspring_list = []
        for i in range(0, number_of_offsprings):
            child_model = self.create_model()
            child_model.layers[0].set_weights([offspring_weights, self.bias])
            child_model.compile(optimizer='adam', loss=None, metrics=None)
            offspring_list.append(child_model)
        return offspring_list


def fitness_func(health, steps):
    # Calculate fitness based on health and steps survived
    # Giving 10 percent weightage to health and 90 percent to steps survived
    fitness = (0.1 * health) + (0.9 * steps)
    return fitness


if __name__ == '__main__':
    # Initialize genetic algorithm parameters
    gen = GeneticAlgo((8,), 15, 1, [10], 4, 'relu', 'softmax')
    df = pd.read_csv('genetic_res.csv')  # Read data from CSV file into DataFrame
    nn_gen = gen.nn_creation(5)  # Generate initial population of neural networks
    number_of_generations = 20
    number_of_mutations = 2
    herbivore_no = 5
    carnivore_no = 15
    plant_no = 90
    rock_no = 80
    herbivore_health = 100
    carnivore_health = 100

    for i in range(0, number_of_generations):
        print("Generation: ", i)
        env = Simulation(herbivore_no, carnivore_no, plant_no, rock_no, herbivore_health, carnivore_health,
                         sim_controller="custom", speed=120, available_steps=150)
        herbivore_list, carnivore_list, _, _ = env.get_lists()
        herbi1, herbi2, herbi3, herbi4, herbi5 = herbivore_list[0], herbivore_list[1], herbivore_list[2], \
                                                 herbivore_list[3], \
                                                 herbivore_list[4]
        done = 0
        obs_list = []
        obs = 0
        for o in range(0, herbivore_no):
            ob = np.array([0, 0, 0, 0, 0, 0, 0, 0])
            ob = ob.reshape((-1, 8))
            obs_list.append(ob)
        fitness_list = [0] * herbivore_no
        while done == 0:
            done, obs = env.step(herbi1, np.argmax(nn_gen[0].predict(obs_list[0])) + 1)
            if type(obs) == list:
                obs_list[0] = np.array(obs[0:8]).reshape((-1, 8))
                fitness_list[0] = fitness_func(obs[-2], obs[-1])
            done, obs = env.step(herbi2, np.argmax(nn_gen[0].predict(obs_list[1])) + 1)
            if type(obs) == list:
                obs_list[1] = np.array(obs[0:8]).reshape((-1, 8))
                fitness_list[1] = fitness_func(obs[-2], obs[-1])
            done, obs = env.step(herbi3, np.argmax(nn_gen[0].predict(obs_list[2])) + 1)
            if type(obs) == list:
                obs_list[2] = np.array(obs[0:8]).reshape((-1, 8))
                fitness_list[2] = fitness_func(obs[-2], obs[-1])
            done, obs = env.step(herbi4, np.argmax(nn_gen[0].predict(obs_list[3])) + 1)
            if type(obs) == list:
                obs_list[3] = np.array(obs[0:8]).reshape((-1, 8))
                fitness_list[3] = fitness_func(obs[-2], obs[-1])
            done, obs = env.step(herbi5, np.argmax(nn_gen[0].predict(obs_list[4])) + 1)
            if type(obs) == list:
                obs_list[4] = np.array(obs[0:8]).reshape((-1, 8))
                fitness_list[4] = fitness_func(obs[-2], obs[-1])
            for carni in carnivore_list[-2::-1]:
                done, obs = env.step(carni, random.randint(1, 4))
            # print("Fitness: ", fitness_list)
        dic_res = {'Generation': i, 'Winner': obs, "Fitness": fitness_list}
        df = df._append(dic_res, ignore_index=True)  # Append results to DataFrame
        df.to_csv('genetic_res.csv', index=False)  # Save DataFrame to CSV
        max_index = fitness_list.index(max(fitness_list))
        fitness_list[max_index] = -100
        max_index_2 = fitness_list.index(max(fitness_list))
        parent1 = nn_gen[max_index]
        parent2 = nn_gen[max_index_2]
        child_weights = gen.crossing(parent1, parent2, number_of_mutations)
        nn_gen = gen.create_offsprings(child_weights, herbivore_no)
    print("Genetic Search DONE")
