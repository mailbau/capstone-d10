import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random
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
    G.add_edge(edge[1], edge[0], weight=distance)  # Ensure bidirectional edges

def heuristic(node1, node2):
    x1, y1 = nodes[node1]
    x2, y2 = nodes[node2]
    return np.sqrt((x1 - x2)**2 + (y1 - y2)**2)

class AntColony:
    def __init__(self, G, nodes, bin_capacities, vehicle_capacity, n_ants, n_best, n_iterations, decay, alpha=1, beta=1):
        self.G = G
        self.nodes = nodes
        self.bin_capacities = bin_capacities
        self.vehicle_capacity = vehicle_capacity
        self.n_ants = n_ants
        self.n_best = n_best
        self.n_iterations = n_iterations
        self.decay = decay
        self.alpha = alpha
        self.beta = beta
        self.pheromone = {edge: 1 for edge in self.G.edges}
        self.all_edges = list(self.G.edges)  # Store all edges for reference

    def run(self):
        shortest_path = None
        all_time_shortest_path = ("placeholder", np.inf)
        for i in range(self.n_iterations):
            all_paths = self.gen_all_paths()
            self.spread_pheromone(all_paths, self.n_best, shortest_path=shortest_path)
            shortest_path = min(all_paths, key=lambda x: x[1])
            if shortest_path[1] < all_time_shortest_path[1]:
                all_time_shortest_path = shortest_path            
            self.pheromone_decay()
        return all_time_shortest_path

    def gen_all_paths(self):
        all_paths = []
        for i in range(self.n_ants):
            path = self.gen_path('Garage', 'Destination')
            all_paths.append((path, self.calc_path_distance(path)))
        return all_paths

    def gen_path(self, start_node, end_node):
        path = [start_node]
        nodes_to_visit = set(self.nodes.keys())
        nodes_to_visit.remove(start_node)
        nodes_to_visit.remove(end_node)
        current_node = start_node
        current_load = 0

        while nodes_to_visit:
            next_node = self.pick_next_node(current_node, nodes_to_visit)
            if next_node in self.bin_capacities:
                current_load += self.bin_capacities[next_node]
                if current_load > self.vehicle_capacity:
                    break
            if next_node != end_node:
                path.append(next_node)
                nodes_to_visit.remove(next_node)
                current_node = next_node

        path.append(end_node)
        return path

    def pick_next_node(self, current_node, nodes_to_visit):
        pheromone = []
        heuristics = []
        for node in nodes_to_visit:
            try:
                pheromone.append(self.pheromone[(current_node, node)])
            except KeyError:
                pheromone.append(self.pheromone[(node, current_node)])
            heuristics.append(1 / nx.astar_path_length(self.G, current_node, node, heuristic=heuristic))
        pheromone = np.array(pheromone) ** self.alpha
        heuristics = np.array(heuristics) ** self.beta
        probs = pheromone * heuristics
        probs /= probs.sum()
        return np.random.choice(list(nodes_to_visit), p=probs)

    def spread_pheromone(self, all_paths, n_best, shortest_path):
        sorted_paths = sorted(all_paths, key=lambda x: x[1])
        for path, dist in sorted_paths[:n_best]:
            for i in range(len(path) - 1):
                move = (path[i], path[i + 1])
                if move in self.pheromone:
                    self.pheromone[move] += 1.0 / dist
                else:
                    reverse_move = (move[1], move[0])
                    if reverse_move in self.pheromone:
                        self.pheromone[reverse_move] += 1.0 / dist

    def pheromone_decay(self):
        for edge in self.pheromone:
            self.pheromone[edge] *= self.decay

    def calc_path_distance(self, path):
        total_dist = 0
        for i in range(len(path) - 1):
            total_dist += nx.astar_path_length(self.G, path[i], path[i + 1], heuristic=heuristic)
        return total_dist

if __name__ == "__main__":
    start_time = time.time()

    ant_colony = AntColony(G, nodes, bin_capacities, vehicle_capacity, 10, 5, 10, 0.95, alpha=1, beta=2)
    shortest_path, distance = ant_colony.run()
    end_time = time.time()
    execution_time = end_time - start_time

    print("Execution time:", execution_time, "seconds")

    print("Best route: ", shortest_path)
    print("Best distance: ", distance)

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
    best_route_edges = [(shortest_path[i], shortest_path[i+1]) for i in range(len(shortest_path) - 1)]
    nx.draw_networkx_edges(G, pos, edgelist=best_route_edges, edge_color='r', width=2)
    
    plt.title('CVRP Best Route Found by Ant Colony Optimization')
    plt.show()
