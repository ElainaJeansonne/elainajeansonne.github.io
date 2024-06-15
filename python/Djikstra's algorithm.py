# Define the adjacency matrix
adjacency_matrix = [
    [0, 3, 0, 0, 7, 0, 5, 0, 0],
    [3, 0, 7, 0, 1, 0, 0, 0, 0],
    [0, 7, 0, 1, 2, 2, 0, 0, 0],
    [0, 0, 1, 0, 0, 3, 0, 0, 5],
    [7, 1, 2, 0, 0, 1, 3, 3, 0],
    [0, 0, 2, 3, 1, 0, 0, 3, 2],
    [5, 0, 0, 0, 3, 0, 0, 2, 0],
    [0, 0, 0, 0, 3, 3, 2, 0, 4],
    [0, 0, 0, 5, 0, 2, 0, 4, 0]
]

# Function to find the shortest path using Dijkstra's algorithm
def dijkstra(adjacency_matrix, source):
    num_vertices = len(adjacency_matrix)
    distance = [float('inf')] * num_vertices
    distance[source] = 0
    visited = [False] * num_vertices

    for _ in range(num_vertices):
        # Find the vertex with the minimum distance
        min_distance = float('inf')
        min_vertex = -1
        for v in range(num_vertices):
            if not visited[v] and distance[v] < min_distance:
                min_distance = distance[v]
                min_vertex = v
        visited[min_vertex] = True

        # Update the distances to the neighboring vertices
        for v in range(num_vertices):
            if (
                not visited[v] and
                adjacency_matrix[min_vertex][v] != 0 and
                distance[min_vertex] + adjacency_matrix[min_vertex][v] < distance[v]
            ):
                distance[v] = distance[min_vertex] + adjacency_matrix[min_vertex][v]

    return distance

# Find the shortest paths from vertex 0 to all other vertices
source_vertex = 0
shortest_paths = dijkstra(adjacency_matrix, source_vertex)

# Display the shortest paths
for target_vertex, shortest_distance in enumerate(shortest_paths):
    if target_vertex != source_vertex:
        print(f"Shortest path from vertex {source_vertex} to vertex {target_vertex}:")
        if shortest_distance == float('inf'):
            print("No path exists.")
        else:
            path = [target_vertex]
            while path[-1] != source_vertex:
                current_vertex = path[-1]
                for v, weight in enumerate(adjacency_matrix[current_vertex]):
                    if weight > 0 and shortest_paths[current_vertex] - weight == shortest_paths[v]:
                        path.append(v)
                        break
            path.reverse()
            print(f" -> ".join(str(vertex) for vertex in path))
        print(f"Shortest distance: {shortest_distance}")
        print()

The code needs to plot a weighted graph of the solution.  The indices in the code must be updated to start at 1, so add 1 to all the indices and update all references to those indices. The function definitions must be at the end of the file, after all other statements.  Here is the Python code: