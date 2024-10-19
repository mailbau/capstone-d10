import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import time


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

def heuristic(node1, node2):
    x1, y1 = nodes[node1]
    x2, y2 = nodes[node2]
    return np.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def evalCVRP_Astar():
    best_route = None
    best_distance = float('inf')

    node_names = list(nodes.keys())[1:-1]  # Exclude 'Garage' and 'Destination'
    n = len(node_names)

    for perm in permutations(node_names):
        current_route = ['Garage'] + list(perm) + ['Destination']
        current_distance = 0
        current_load = 0
        valid_route = True

        for i in range(len(current_route) - 1):
            if current_route[i] in bin_capacities:
                current_load += bin_capacities[current_route[i]]
            if current_load > vehicle_capacity:
                valid_route = False
                break
            try:
                path_length = nx.astar_path_length(G, current_route[i], current_route[i+1], heuristic=heuristic)
            except nx.NetworkXNoPath:
                valid_route = False
                break
            current_distance += path_length
        
        if valid_route and current_distance < best_distance:
            best_route = current_route
            best_distance = current_distance
    
    return best_route, best_distance

from itertools import permutations

if __name__ == "__main__":
    start_time = time.time()
    best_route, best_distance = evalCVRP_Astar()
    end_time = time.time()
    execution_time = end_time - start_time

    print("Execution time:", execution_time, "seconds")
    
    print("Best route: ", best_route)
    print("Best distance: ", best_distance)

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
    
    plt.title('CVRP Best Route Found by A*')
    plt.show()
