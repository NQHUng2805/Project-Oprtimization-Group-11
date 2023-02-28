import copy
import random
import numpy as np
from collections import defaultdict
import time
from collections import deque
import generate_sample
# from ortools.sat.python import cp_model
import time

# Import algorithms
import greedy
import hill_climbing



def random_configuration(num_buses, num_passengers):
    def random_conf(num_buses, num_passengers):
        configuration = defaultdict(lambda: [0])
        for passenger in range(num_passengers):
            bus = np.random.choice(num_buses, 1)[0]
            configuration[bus + 1].append(passenger + 1)
            configuration[bus + 1].append(passenger + 1 + num_passengers)
        return configuration

    def uniform_random_conf(num_buses, num_passengers):

        configuration = defaultdict(lambda: [0])
        arr = np.arange(1, num_passengers + 1)
        np.random.shuffle(arr)
        split_passengers = np.array_split(arr, num_buses)
        for bus in range(num_buses):
            single_conf = split_passengers[bus].tolist()
            for passenger in split_passengers[bus]:
                single_conf.append(passenger + num_passengers)
            configuration[bus + 1].extend(sorted(single_conf))
        return configuration

    confs = random_conf(num_buses, num_passengers)
    uniform_confs = uniform_random_conf(num_buses, num_passengers)

    return uniform_confs


def generate_distance_matrix(matrix_dist, list_passengers):
    return matrix_dist[list_passengers, :][:, list_passengers]


def decode_cities(list_passengers, config):
    new_config = list()
    for c in range(len(config)):
        new_config.append(list_passengers[config[c]])
    return new_config


# Data sample
# matrix_distance = np.array([[0, 7, 7, 7, 6, 7, 7, 9, 7, 7, 9],
#                             [5, 0, 6, 5, 8, 7, 5, 5, 8, 8, 8],
#                             [7, 8, 0, 8, 9, 7, 8, 7, 7, 6, 9],
#                             [8, 8, 9, 0, 6, 8, 9, 5, 8, 8, 5],
#                             [5, 6, 6, 9, 0, 7, 6, 9, 5, 8, 9],
#                             [6, 9, 8, 6, 5, 0, 6, 7, 6, 5, 9],
#                             [8, 9, 7, 7, 6, 6, 0, 7, 6, 9, 5],
#                             [5, 6, 7, 8, 8, 8, 7, 0, 9, 5, 6],
#                             [6, 5, 9, 8, 7, 8, 6, 8, 0, 9, 7],
#                             [6, 6, 9, 5, 8, 5, 6, 5, 8, 0, 8],
#                             [7, 6, 9, 7, 5, 5, 5, 8, 7, 5, 0]])


if __name__ == "__main__":
    num_cities = 31
    num_buses = 3
    buses_capacities = [2, 3, 3]

    matrix_distance = np.array(generate_sample.generate_sample(num_cities)[0])
    num_passengers = int((len(matrix_distance) - 1) / 2)

    dict_schedules = random_configuration(num_buses, num_passengers)

    branch_bound_cost = 0
    greedy_cost = 0
    hill_climbing_cost = 0
    uc_cost = 0
    randomized_travel_cost = 0
    beam_cost = 0
    ga_cost = 0

    hl_start_time = time.time()
    for id_bus, schedule in dict_schedules.items():
        # Generate matrix distance of id_bus
        matrix_dist_of_a_bus = generate_distance_matrix(matrix_distance, schedule)
        num_cities = np.shape(matrix_dist_of_a_bus)[0]
        # (Metaheuristic) Hill Climbing algorithm
        Hill_Climbing = hill_climbing.Graph_Hill_Climbing(num_cities, matrix_dist_of_a_bus, buses_capacities[id_bus - 1])
        hl = Hill_Climbing.Metaheuristic_Hill_Climbing()
        hill_climbing_cost += hl[0]
        opti_schedule = decode_cities(schedule, hl[1])
        print(f"Bus ID {id_bus}, schedule: {opti_schedule}")
    time_hl = time.time() - hl_start_time
    print(f"Metaheuristic Hill Climbing algorithm, cost: {hill_climbing_cost}, time: {round(time_hl, 4)} second")