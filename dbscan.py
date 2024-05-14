import pygame
import math

# Экран
WIDTH, HEIGHT = 800, 600
FPS = 30

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

# Настройки DBSCAN
EPS = 40
MIN_PTS = 5


# Класс точки
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = BLACK
        self.cluster = -1

    def distance(self, point2):
        return math.sqrt((self.x - point2.x)**2 + (self.y - point2.y)**2)


# Класс DBSCAN
# class DBSCAN:
#     def __init__(self, eps, minPts):
#         self.eps = eps
#         self.minPts = minPts
#
#     def fit(self, data):
#         markers = [0] * len(data)
#         cluster_id = 1
#
#         for i in range(len(data)):
#             if markers[i] != 0:
#                 continue
#
#             neighbors = self.get_neighbors(data, i)
#             if len(neighbors) < self.minPts:
#                 markers[i] = -1
#                 continue
#
#             self.expand_cluster(data, i, neighbors, markers, cluster_id)
#             cluster_id += 1
#
#         return markers
#
#     def get_neighbors(self, data, i):
#         neighbors = []
#         for j in range(len(data)):
#             if i == j:
#                 continue
#             if self.distance(data[i], data[j]) <= self.eps:
#                 neighbors.append(j)
#         return neighbors
#
#     def expand_cluster(self, data, i, neighbors, markers, cluster_id):
#         markers[i] = cluster_id
#         for j in neighbors:
#             if markers[j] == -1:
#                 markers[j] = cluster_id
#             elif markers[j] == 0:
#                 markers[j] = cluster_id
#                 new_neighbors = self.get_neighbors(data, j)
#                 if len(new_neighbors) >= self.minPts:
#                     neighbors.extend(new_neighbors)
#
#     def distance(self, a, b):
#         dx = a.x - b.x
#         dy = a.y - b.y
#         return math.sqrt(dx * dx + dy * dy)
#
#     def get_marker(self, clusters):
#         markers = [-1] * len(clusters)
#
#         for j in range(len(clusters)):
#             for k in range(len(clusters[j])):
#                 if not clusters[j]:
#                     continue
#
#                 if clusters[j][k] == -1:
#                     markers[j] = clusters[j][k]
#                 else:
#                     markers[clusters[j][k]] = j
#
#         return markers


# Настройка pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Точки
points = []

# Работа с точками
running = True
adding_points = False
marking_points = False
markers = [-1] * len(points)
while running:
    # События
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                adding_points = True
            elif event.button == 3:
                marking_points = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                adding_points = False
            elif event.button == 3:
                marking_points = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ENTER:
                clusters = []
                for i in range(len(points)):
                    if markers[i] == -1:
                        new_cluster = [i]
                        cluster_id = len(clusters) + 1
                        markers[i] = cluster_id
                        clusters.append(new_cluster)
                        neighbors = [j for j in range(len(points)) if j != i and points[i].distance(points[j]) <= EPS]
                        if len(neighbors) >= MIN_PTS:
                            for j in neighbors:
                                if markers[j] == -1:
                                    new_cluster.append(j)
                                    markers[j] = cluster_id
                                    for j in range(len(clusters)):
                                        for k in range(len(clusters[j])):
                                            if not clusters[j]:
                                                continue

                                            if clusters[j][k] == -1:
                                                markers[j] = clusters[j][k]
                                            else:
                                                markers[clusters[j][k]] = j
                                    for i in range(len(points)):
                                        if markers[i] == -1:
                                            points[i].color = RED
                                        else:
                                            points[i].cluster = markers[i]
                                            points[i].color = GREEN

                                        # Добавление точек
                                    if adding_points:
                                        x, y = pygame.mouse.get_pos()
                                        points.append(Point(x, y))
                                        markers.append(-1)

                                        # Маркировка точек
                                    if marking_points:
                                        x, y = pygame.mouse.get_pos()
                                        for i in range(len(points)):
                                            if points[i].distance((x, y)) <= 5:
                                                if markers[i] == -1:
                                                    markers[i] = 0
                                                elif markers[i] == 0:
                                                    markers[i] = -1

                                        # Отрисовка
                                    screen.fill(BLACK)
                                    for point in points:
                                        pygame.draw.circle(screen, point.color, (point.x, point.y), 3)

                                    # Обновление экрана
                                    pygame.display.update()

                                    # FPS
                                    clock.tick(FPS)

                            # Закрытие pygame
                            pygame.quit()