import heapq
from collections import defaultdict
from math import sqrt

# Expanded list of points with coordinates and demands
point_dict = [
    {"point": 0, "name": "Start", "coordinates": (0, 0), "demand": 0.0},
    {"point": 1, "name": "Point1", "coordinates": (1, 1), "demand": 5.0},
    {"point": 2, "name": "Point2", "coordinates": (2, 2), "demand": 3.0},
    {"point": 3, "name": "Point3", "coordinates": (3, 1), "demand": 4.0},
    {"point": 4, "name": "Point4", "coordinates": (4, 3), "demand": 6.0},
    {"point": 5, "name": "Point5", "coordinates": (5, 0), "demand": 2.0},
    {"point": 6, "name": "Point6", "coordinates": (6, 2), "demand": 4.0},
    {"point": 7, "name": "Point7", "coordinates": (7, 1), "demand": 3.5},
    {"point": 8, "name": "Goal", "coordinates": (8, 0), "demand": 0.0},
]

# Expanded list of paths with distances between points
path_dict = [
    {"path_id": 0, "start_id": 0, "end_id": 1, "distance": 1.5},
    {"path_id": 1, "start_id": 1, "end_id": 2, "distance": 1.0},
    {"path_id": 2, "start_id": 2, "end_id": 3, "distance": 1.2},
    {"path_id": 3, "start_id": 3, "end_id": 4, "distance": 1.4},
    {"path_id": 4, "start_id": 4, "end_id": 5, "distance": 2.1},
    {"path_id": 5, "start_id": 5, "end_id": 6, "distance": 1.3},
    {"path_id": 6, "start_id": 6, "end_id": 7, "distance": 0.9},
    {"path_id": 7, "start_id": 7, "end_id": 8, "distance": 1.6},
    {"path_id": 8, "start_id": 0, "end_id": 4, "distance": 2.5},
    {"path_id": 9, "start_id": 1, "end_id": 3, "distance": 1.1},
    {"path_id": 10, "start_id": 2, "end_id": 6, "distance": 1.8},
    {"path_id": 11, "start_id": 4, "end_id": 7, "distance": 2.4},
    {"path_id": 12, "start_id": 3, "end_id": 5, "distance": 1.7},
    {"path_id": 13, "start_id": 5, "end_id": 8, "distance": 2.0},
    {"path_id": 14, "start_id": 6, "end_id": 8, "distance": 1.5},
    {"path_id": 15, "start_id": 8, "end_id": 0, "distance": 10.5},
]


class AStarAlgorithm:
    def __init__(self, point_dict, path_dict, max_capacity, weights=(0.4, 0.3, 0.3), static_endpoints_name=None):
        self.points = {p['point']: p for p in point_dict}
        self.edges = defaultdict(list)
        self.max_capacity = max_capacity
        self.weights = list(weights)  # Dynamic weights
        self.path_dict = path_dict
        self.point_dict = point_dict
        self.static_endpoints_name = static_endpoints_name

        # Create edges from path_dict using given distances
        for path in path_dict:
            start, end, distance = path['start_id'], path['end_id'], path['distance']
            self.edges[start].append((end, distance))
            self.edges[end].append((start, distance))  # Bidirectional graph

    def heuristic(self, current, goal, accumulated_demand):
        # Minimize unused capacity
        unused_capacity = max(self.max_capacity - accumulated_demand, 0)

        # Minimize occupancy ratio between nodes
        occupancy_ratio = 1 / (accumulated_demand / self.max_capacity) if accumulated_demand > 0 else 0

        # Minimize path distance (using direct path if exists or minimal path distance)
        route_distance = self.get_min_path_distance(current, goal)

        # Objective function calculation
        objective_value = (self.weights[0] * unused_capacity +
                           self.weights[1] * occupancy_ratio +
                           self.weights[2] * route_distance)
        return objective_value

    def get_min_path_distance(self, start, end):
        # Check if a direct edge exists
        for neighbor, dist in self.edges[start]:
            if neighbor == end:
                return dist

        # Estimate minimal distance if direct path is unavailable
        visited = set()
        min_heap = [(0, start)]
        while min_heap:
            dist, node = heapq.heappop(min_heap)
            if node == end:
                return dist
            if node in visited:
                continue
            visited.add(node)
            for neighbor, edge_dist in self.edges[node]:
                if neighbor not in visited:
                    heapq.heappush(min_heap, (dist + edge_dist, neighbor))
        return float('inf')  # if no path exists

    def a_star_search(self, start, goal):
        open_set = []
        heapq.heappush(open_set, (0, start))

        g_costs = {start: 0}
        came_from = {start: None}

        best_path = []
        best_objective_value = float('inf')

        while open_set:
            _, current = heapq.heappop(open_set)
            if current == goal:
                best_path = self.reconstruct_path(came_from, current)
                best_objective_value = self.calculate_objective_value(best_path)
                break

            for neighbor, distance in self.edges[current]:
                new_g_cost = g_costs[current] + distance
                path_to_current = self.reconstruct_path(came_from, current)
                accumulated_demand = sum(self.points[n]['demand'] for n in path_to_current)

                if accumulated_demand + self.points[neighbor]['demand'] > self.max_capacity:
                    continue

                if neighbor not in g_costs or new_g_cost < g_costs[neighbor]:
                    g_costs[neighbor] = new_g_cost
                    h_cost = self.heuristic(neighbor, goal, accumulated_demand + self.points[neighbor]['demand'])
                    f_cost = new_g_cost + h_cost
                    heapq.heappush(open_set, (f_cost, neighbor))
                    came_from[neighbor] = current

        if best_path:
            unused_capacity, occupancy_ratio, total_distance = self.calculate_contributions(best_path)

        if self.static_endpoints_name:
            point_id = [
                point['point'] for point in self.point_dict if point['name'].lower() == self.static_endpoints_name.lower()
            ]
            best_path += [point_id[0]]
            additional_distance = [path['distance'] for path in self.path_dict if path['start_id'] == best_path[-2] and path['end_id'] == best_path[-1]]
            total_distance += additional_distance[0]

        return {
            "path": self.generate_path_data(best_path), 
            "objective_value": best_objective_value,
            "unused_capacity": unused_capacity,
            "occupancy_ratio": occupancy_ratio,
            "total_distance": total_distance}

    def reconstruct_path(self, came_from, current):
        path = []
        while current is not None:
            path.append(current)
            current = came_from[current]
        return path[::-1]

    def calculate_objective_value(self, path):
        accumulated_demand = 0
        total_distance = 0
        occupancy_ratio = 0

        for i in range(len(path) - 1):
            start, end = path[i], path[i + 1]
            accumulated_demand += self.points[end]['demand']
            distance = next((dist for neighbor, dist in self.edges[start] if neighbor == end), 0)
            total_distance += distance
            occupancy_ratio += 1 / (accumulated_demand / self.max_capacity) if accumulated_demand > 0 else 0

        unused_capacity = max(self.max_capacity - accumulated_demand, 0)
        objective_value = (self.weights[0] * unused_capacity +
                           self.weights[1] * occupancy_ratio +
                           self.weights[2] * total_distance)

        print(f"Objective value for path {path}: {objective_value}")
        return objective_value

    def calculate_contributions(self, path):
        accumulated_demand = 0
        total_distance = 0
        occupancy_ratio = 0

        for i in range(len(path) - 1):
            start, end = path[i], path[i + 1]
            accumulated_demand += self.points[end]['demand']
            distance = next((dist for neighbor, dist in self.edges[start] if neighbor == end), 0)
            total_distance += distance
            occupancy_ratio += 1 / (accumulated_demand / self.max_capacity) if accumulated_demand > 0 else 0

        unused_capacity = max(self.max_capacity - accumulated_demand, 0)
        print(f"Contributions for path {path}:\nUnused Capacity: {unused_capacity}, Occupancy Ratio: {occupancy_ratio}, Total Distance: {total_distance}")
        return unused_capacity, occupancy_ratio, total_distance
    
    def generate_path_data(self, path):
        path_data = []
        for i in range(len(path) - 1):
            start, end = path[i], path[i + 1]
            distance = next((path['distance'] for path in self.path_dict if path['start_id'] == start and path['end_id'] == end), None)
            path_id = next((path['path_id'] for path in self.path_dict if path['start_id'] == start and path['end_id'] == end), None)
            path_data.append({
                "start": self.points[start],
                "end": self.points[end],
                "distance": distance,
                "path_id": path_id
            })
        return path_data
    
    def __call__(self, start):
        objective_values = []
        path_data = []
        for data in self.point_dict:
            try:
                result = self.a_star_search(start, data['point'])
                objective_values.append(result['objective_value'])
                path_data.append(result)
            except Exception as _:
                continue
        min_objective_value = min(objective_values)
        min_index = objective_values.index(min_objective_value)
        return path_data[min_index]


# Initialize parameters
max_capacity = 11.0  # Maximum vehicle capacity

weights=(0.4, 0.4, 0.2)

# Instantiate and run the A* algorithm
a_star = AStarAlgorithm(point_dict, path_dict, max_capacity, weights)
start_point = 0  # Define starting point
goal_point = 8  # Define goal point
# result = a_star.a_star_search(start_point, goal_point)
result = a_star(start_point)

# Output the result
print("Optimal path:", result["path"])
print("Objective value:", result["objective_value"])
print("Unused capacity:", result["unused_capacity"])
print("Occupancy ratio:", result["occupancy_ratio"])
print("Total distance:", result["total_distance"])
