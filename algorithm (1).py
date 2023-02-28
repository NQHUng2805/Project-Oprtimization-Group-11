
import copy
import numpy as np
def optimal_path(num_cities, matrix):
    res = list()
    num_startcities = int(num_cities / 2)

    def invariant_TSP(num_cities, num_startcities, mat, seen_cities = list(), prev_city = 0, configuration = [0], cost = 0):
        for city in range(1, num_cities+1):
            if city not in seen_cities:
                if city > num_startcities:
                    start_city = city - num_startcities
                    if start_city not in seen_cities:
                        continue
                
                new_cost = cost + mat[prev_city][city]
                seen_cities.append(city)
                configuration.append(city)

                if len(configuration) == num_cities + 1:
                    configuration.append(0)
                    new_cost = new_cost + mat[city][0]
                    res.append([new_cost, configuration])
                    break
                
                else:#city is depot???
                    new_seen_cities = copy.deepcopy(seen_cities)
                    new_configuration = copy.deepcopy(configuration)
                    invariant_TSP(num_cities, num_startcities, mat, new_seen_cities, city, new_configuration, new_cost)
                    seen_cities = seen_cities[:-1]
                    configuration = configuration[:-1]
                
    invariant_TSP(num_cities, num_startcities, matrix)
    res.sort(key = lambda x: x[0])
    return res[0]


            