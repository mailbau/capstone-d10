import heapq
from collections import defaultdict


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
        if isinstance(start, str):
            start = [point['point'] for point in self.point_dict if point['name'].lower() == start.lower()][0]
        if isinstance(goal, str):
            goal = [point['point'] for point in self.point_dict if point['name'].lower() == goal.lower()][0]
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
            "path_list": best_path,
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

        # print(f"Objective value for path {path}: {objective_value}")
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
        # print(f"Contributions for path {path}:\nUnused Capacity: {unused_capacity}, Occupancy Ratio: {occupancy_ratio}, Total Distance: {total_distance}")
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
        unused_capacity_values = []
        path_data = []
        for data in self.point_dict:
            try:
                result = self.a_star_search(start, data['point'])
                objective_values.append(result['objective_value'])
                unused_capacity_values.append(result['unused_capacity'])
                path_data.append(result)
            except Exception as _:
                continue
        min_unused_capacity_values = min(unused_capacity_values)
        min_index = unused_capacity_values.index(min_unused_capacity_values)
        return path_data[min_index]