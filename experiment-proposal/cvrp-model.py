import networkx as nx
import matplotlib.pyplot as plt

# Create a graph
G = nx.Graph()

# Define nodes
nodes = {
    'Garage': (0, 0),  # Starting point
    'Bin1': (1, 2),
    'Bin2': (3, 1),
    'Bin3': (4, 4),
    'Destination': (6, 0)  # Final destination
}

# Define bin capacities
bin_capacities = {
    'Bin1': 2,
    'Bin2': 3,
    'Bin3': 1
}

# Define vehicle capacity
vehicle_capacity = 4

# Add nodes with positions (for visualization)
G.add_nodes_from(nodes.keys())

# Define distances (satisfying the triangle inequality)
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

# Add edges with weights (distances)
for edge, distance in distances.items():
    G.add_edge(edge[0], edge[1], weight=distance)

# Draw the graph
pos = nodes
nx.draw(G, pos, with_labels=False, node_size=700, node_color='lightblue', font_size=12, font_weight='bold')

# Draw edge labels (weights/distances)
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

# Add capacity labels to the bins
bin_labels = {node: f'{node}\nCapacity: {cap}' for node, cap in bin_capacities.items()}
bin_labels['Garage'] = 'Garage\nStart'
bin_labels['Destination'] = 'Destination\nEnd'

# Draw node labels with capacities
nx.draw_networkx_labels(G, pos, labels=bin_labels, font_size=10)

plt.title('CVRP Model Illustration')
plt.show()
