import random
import time
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from deap import base, creator, tools, algorithms

# Define the graph
G = nx.Graph()

nodes = {
    'Garage': (0, 0),  # Starting point
    'Bin1': (1, 2),
    'Bin2': (3, 1),
    'Bin3': (4, 4),
    'Destination': (6, 0)  # Final destination
}

bin_capacities = {
    'Bin1': 2,
    'Bin2': 3,
    'Bin3': 1
}

vehicle_capacity = 10

distances = {
    ('Garage', 'Bin1'): 2.24,
    ('Garage', 'Bin2'): 3.16,
    ('Garage', 'Bin3'): 5.0,
    ('Garage', 'Destination'): 6.0,
    ('Bin1', 'Bin2'): 2.24,
    ('Bin1', 'Bin3'): 3.61,
    ('Bin1', 'Destination'): 5.10,
    ('Bin2', 'Bin3'): 3.61,
    ('Bin2', 'Destination'): 3.16,
    ('Bin3', 'Destination'): 4.0
}

for edge, distance in distances.items():
    G.add_edge(edge[0], edge[1], weight=distance)

# GA setup using DEAP
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
node_names = list(nodes.keys())[1:-1]  # Exclude 'Garage' and 'Destination'
node_indices = list(range(len(node_names)))  # Indices for the nodes

toolbox.register("indices", random.sample, node_indices, len(node_indices))
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.indices)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def evalCVRP(individual):
    route = ['Garage'] + [node_names[i] for i in individual] + ['Destination']
    total_distance = 0
    current_load = 0
    
    for i in range(len(route) - 1):
        if route[i] in bin_capacities:
            current_load += bin_capacities[route[i]]
        if current_load > vehicle_capacity:
            return float('inf'),
        total_distance += G[route[i]][route[i+1]]['weight']
    
    return total_distance,

toolbox.register("mate", tools.cxOrdered)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.2)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("evaluate", evalCVRP)

def main():
    random.seed(42)
    
    pop = toolbox.population(n=100)
    hof = tools.HallOfFame(1)
    
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("min", np.min)
    
    algorithms.eaSimple(pop, toolbox, cxpb=0.7, mutpb=0.2, ngen=100, stats=stats, halloffame=hof, verbose=True)
    
    return pop, stats, hof

if __name__ == "__main__":
    start_time = time.time()
    pop, stats, hof = main()
    
    best_individual = hof[0]
    best_route = ['Garage'] + [node_names[i] for i in best_individual] + ['Destination']
    end_time = time.time()
    execution_time = end_time - start_time

    print("Execution time:", execution_time, "seconds")
    print("Best route: ", best_route)
    print("Best distance: ", evalCVRP(best_individual)[0])

    # Draw the best route
    pos = nodes
    nx.draw(G, pos, with_labels=False, node_size=700, node_color='lightblue', font_size=12, font_weight='bold')
    
    # Draw edges and node labels
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    bin_labels = {node: f'{node}\nCapacity: {cap}' for node, cap in bin_capacities.items()}
    bin_labels['Garage'] = 'Garage\nStart'
    bin_labels['Destination'] = 'Destination\nEnd'
    nx.draw_networkx_labels(G, pos, labels=bin_labels, font_size=10)
    
    # Highlight the best route
    best_route_edges = [(best_route[i], best_route[i+1]) for i in range(len(best_route) - 1)]
    nx.draw_networkx_edges(G, pos, edgelist=best_route_edges, edge_color='r', width=2)
    
    plt.title('CVRP Best Route Found by GA')
    plt.show()
