import random
import pandas as pd

def compute_total_cost(medoids, dist_matrix):
    """Compute the total cost (sum of distances to the nearest medoid)."""
    total_cost = 0.0
    for i in range(len(dist_matrix)):
        min_dist = min(dist_matrix[i][m] for m in medoids)
        total_cost += min_dist
    return total_cost

def k_medoids(labels, dist_matrix, K, max_iter=100):
    """Compute K clusters mased on distance in the dist_matrix such that the centroid of each cluster is a member of the set"""
    N = len(labels)
    if K <= 0 or K > N:
        raise ValueError("K must be between 1 and the number of points")
    
    # Initialize medoids randomly
    medoids = random.sample(range(N), K)
    current_cost = compute_total_cost(medoids, dist_matrix)
    
    # Iterate until convergence or max_iter
    for _ in range(max_iter):
        best_medoids = medoids
        best_cost = current_cost
        improved = False
        
        # Try swapping each medoid with each non-medoid
        for medoid_idx in range(K):
            for point in range(N):
                if point in medoids:
                    continue
                
                # Create new medoids by swapping
                new_medoids = medoids.copy()
                new_medoids[medoid_idx] = point
                new_cost = compute_total_cost(new_medoids, dist_matrix)
                
                # Update if cost improves
                if new_cost < best_cost:
                    best_medoids = new_medoids
                    best_cost = new_cost
                    improved = True
        
        # Break if no improvement
        if not improved:
            break
            
        medoids = best_medoids
        current_cost = best_cost
    
    # Build final clusters
    clusters = [[] for _ in range(K)]
    medoid_labels = [labels[m] for m in medoids]
    
    for i in range(N):
        distances = [dist_matrix[i][m] for m in medoids]
        closest_medoid_idx = distances.index(min(distances))
        clusters[closest_medoid_idx].append(labels[i])
    
    return clusters, medoid_labels


dist_matrix=pd.read_csv('data/coint_pairwise_data.csv')[['Variable1','Variable2','ADF Statistic']]
dist_matrix=dist_matrix.pivot(index='Variable1', columns='Variable2', values='ADF Statistic')
dist_matrix=dist_matrix.fillna(0.0)
dist_matrix=dist_matrix.apply(lambda x:abs(x))
n_clusters=5


labels = dist_matrix.index.tolist()

# 2. Reorder columns to match index order (critical step!)
dist_df_reordered = dist_matrix[labels]

# 3. Convert to 2D list (N x N matrix)
dist_matrix = dist_df_reordered.values.tolist()

labels, medoids = k_medoids(labels , dist_matrix, n_clusters, 100)

for l in labels:
    print (l)
