import numpy as np
import matplotlib.pyplot as plt


class DBSCAN:
    def __init__(self, epsilon=1, min_pts=5):
        self.epsilon = epsilon
        self.min_pts = min_pts
        self.clusters = []
        self.noise = []

    @staticmethod
    def _euclidean_distance(point1, point2):
        print("point1 ", point1)
        print("point2 ", point2)
        return np.sqrt(np.sum((point1 - point2) ** 2))

    def _get_neighbors(self, dataset, point):
        neighbors = []
        for index, candidate in enumerate(dataset):
            print("candidate ", candidate, index)
            if self._euclidean_distance(point, candidate) < self.epsilon:
                neighbors.append(index)
        print("neighbors ", neighbors)
        return neighbors

    def fit(self, dataset):
        visited = [False] * len(dataset)
        for index in range(len(dataset)):
            if not visited[index]:
                visited[index] = True
                neighbors = self._get_neighbors(dataset, dataset[index])
                if len(neighbors) < self.min_pts:
                    self.noise.append(index)
                else:
                    self._expand_cluster(dataset, visited, index, neighbors)
        print("noise ", self.noise)
        print("cluster ", self.clusters)
        return self.clusters, self.noise

    def _expand_cluster(self, dataset, visited, index, neighbors):
        self.clusters.append([index])
        i = 0
        while i < len(neighbors):
            next_index = neighbors[i]
            if not visited[next_index]:
                visited[next_index] = True
                next_neighbors = self._get_neighbors(dataset, dataset[next_index])
                if len(next_neighbors) >= self.min_pts:
                    neighbors += next_neighbors
            cluster_indices = [i for cluster in self.clusters for i in cluster]
            if next_index not in cluster_indices:
                self.clusters[-1].append(next_index)
            i += 1

    def plot(self, dataset):
        plt.figure(figsize=(10, 10))
        colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
        for i, indices in enumerate(self.clusters):
            points = dataset[indices]
            plt.scatter(points[:, 0], points[:, 1], c=colors[i % len(colors)])
        noise_points = dataset[self.noise]
        plt.scatter(noise_points[:, 0], noise_points[:, 1], c='black')
        plt.show()


np.random.seed(0)
cluster1 = np.random.normal(5, 2, size=(50, 2))
cluster2 = np.random.normal(15, 3, size=(50, 2))
cluster3 = np.random.normal(8, 2, size=(50, 2))
dataset = np.concatenate((cluster1, cluster2, cluster3))

dbscan = DBSCAN(epsilon=3, min_pts=5)
clusters, noise = dbscan.fit(dataset)

dbscan.plot(dataset)
