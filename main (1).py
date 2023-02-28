

import algorithm
import configuration
import copy 
import data
N=3
K=3
H=[[4,5],[5,6],[4,5,6]]
matrix_distance = [[0,7,7,5,7,5.6,7],
                   [0,0,10,11.2,10,10.3,14],
                   [0, 10, 0, 5, 14, 2.5, 10],
                   [0, 11.2, 5, 0, 11.2, 2.5, 5],
                   [0, 10, 14, 11.2, 0, 12.5, 10],
                   [0, 10.3, 2.5, 2.5, 12.5, 0, 7.5],
                   [0, 14, 10, 5, 10, 7.5, 0]]

num_capacity = [2,3]
num_buses = 2

print(f"Distance matrix: {matrix_distance}")
print(f"Number of buses: {num_buses}")

num_passengers = int((len(matrix_distance) - 1) / 2)

carriages = configuration.generate_carriages(num_buses, num_passengers, True)

cnt = 0
optimal_cost = 1e9
optimal_path = list()
for carriage in carriages:
    info = list()
    cnt += 1
    mat_buses = configuration.generate_matrix(carriage, matrix_distance)
    total_cost = 0
    for num_bus in range(len(mat_buses)):
        num_cities = len(mat_buses[num_bus]) - 1
        res = algorithm.optimal_path(num_cities, mat_buses[num_bus])
        total_cost = total_cost + res[0]
        priority_arrange = res[1][:-1]
        list_passengers = carriage[num_bus]
        list_cities = copy.deepcopy(list_passengers)
        for c in range(1, len(list_passengers)):
            list_cities.append(list_passengers[c] + num_passengers)
        path = [0] * len(list_cities)
        for p in range(len(priority_arrange)):
            path[p] = list_cities[priority_arrange[p]]
        path.append(0)
        info.append([num_bus, path, res[0]])
    if total_cost < optimal_cost:
        
        optimal_cost = total_cost
        optimal_path = copy.deepcopy(info)
        
for optimal in optimal_path:
    print(f"Car {optimal[0]+1} 's path: {optimal[1]}, the cost is: {optimal[2]}")
print(f"Optimal cost: {optimal_cost}")


