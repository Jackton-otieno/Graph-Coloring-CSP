
# Function to check if it's safe to color the current vertex
# with the given color
def issafe(vertex, col, adj, color):
    """
    Checks if assigning 'col' to 'vertex' is safe (i.e., no adjacent vertex 
    has the same color).
    """
    for neighbor in adj[vertex]:
        # If adjacent vertex is already colored and has the same color, not safe
        if color[neighbor] != -1 and col == color[neighbor]:
            return False
    return True

# Recursive function to try all colorings
def cancolor(vertex, m, adj, color):
    """
    Recursive backtracking function to find a valid m-coloring starting 
    from the current 'vertex'.
    """
    # Base Case: If all vertices are colored successfully
    if vertex == len(color):
        return True

    # Try all colors from 0 to m-1
    for i in range(m):
        if issafe(vertex, i, adj, color):
            # Tentative assignment
            color[vertex] = i
            
            # Recurse for the next vertex
            if cancolor(vertex + 1, m, adj, color):
                # If the rest can be colored, return true
                return True
            
            # Backtrack: If the current choice fails, unassign the color
            color[vertex] = -1
    
    # No valid coloring found for this vertex
    return False 

# Main function to set up the graph and call coloring logic
def graphColoring(V, edges, m):
    """
    Initializes the graph structure and calls the coloring logic.
    V: Number of vertices
    edges: List of graph edges (tuples)
    m: Number of available colors
    """
    # Initialize adjacency list
    adj = [[] for _ in range(V)]

    # Build adjacency list from edges
    for u, w in edges:
        adj[u].append(w)
        adj[w].append(u)

    # Initialize color array with -1 (uncolored)
    color = [-1] * V
    
    # Start the coloring process from vertex 0
    result = cancolor(0, m, adj, color)
    
    # If a solution is found, print the coloring array as well
    if result:
        print(f"Coloring found using {m} colors: {color}")
    
    return result

# Driver code
if __name__ == "__main__":
    # --- Test Case 1: Complete Graph K4 with m=3 (Should be False) ---
    print("--- Test Case 1: K4 Graph with 3 Colors ---")
    V1 = 4
    # Edges for a K4 (complete graph on 4 vertices)
    edges1 = [[0, 1], [0, 2], [0, 3], [1, 3], [2, 3], [1, 2]] 
    m1 = 3 # Not enough colors (needs 4)

    # Check if the graph can be colored with m colors
    print(f"Can the K4 graph be colored with {m1} colors? ->", 
          "true" if graphColoring(V1, edges1, m1) else "false")
    print("-" * 40)

    # --- Test Case 2: K4 Graph with m=4 (Should be True) ---
    print("--- Test Case 2: K4 Graph with 4 Colors ---")
    V2 = 4
    edges2 = [[0, 1], [0, 2], [0, 3], [1, 3], [2, 3], [1, 2]]
    m2 = 4 # Enough colors (needs 4)

    print(f"Can the K4 graph be colored with {m2} colors? ->", 
          "true" if graphColoring(V2, edges2, m2) else "false")
    print("-" * 40)
    
    # --- Test Case 3: Simple Cycle Graph C4 with m=2 (Should be True) ---
    print("--- Test Case 3: C4 Graph (Cycle) with 2 Colors ---")
    V3 = 4
    # Edges for a C4 (cycle graph 0-1-2-3-0)
    edges3 = [[0, 1], [1, 2], [2, 3], [3, 0]]
    m3 = 2 # Needs 2 colors (it's bipartite)

    print(f"Can the C4 graph be colored with {m3} colors? ->", 
          "true" if graphColoring(V3, edges3, m3) else "false")                  