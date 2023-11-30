import math
from random import random

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np


def draw_fig(graph, positions):
    plt.figure(figsize=(8, 6))
    plt.axis('off')
    nx.draw_networkx(graph, pos=positions, node_size=10, width=0.1, with_labels=False)


def generate_delta(n, points, strength, length):
    max_delta = 0
    maxi = 0
    delta = [0] * n
    for m in range(n):
        ex = 0
        ey = 0
        for i in range(n):
            if i == m:
                continue
            norm = math.sqrt((points[m][0] - points[i][0]) ** 2 + (points[m][1] - points[i][1]) ** 2)
            x_mi = points[m][0] - points[i][0]
            y_mi = points[m][1] - points[i][1]

            ex += strength[m, i] * x_mi * (1.0 - length[m, i] / norm)
            ey += strength[m, i] * y_mi * (1.0 - length[m, i] / norm)

        delta[m] = math.sqrt(ex ** 2 + ey ** 2)
        if delta[m] > max_delta:
            max_delta = delta[m]
            maxi = m

    return maxi, delta


def kk_layout(G, flag):
    distances = np.array(nx.floyd_warshall_numpy(G, nodelist=G.nodes()))
    num_nodes = len(G.nodes())
    max_dist = 0

    # Calculating maximum distance
    for i in range(num_nodes):
        for j in range(num_nodes):
            if max_dist < distances[i, j]:
                max_dist = distances[i, j]

    len_0 = 1
    k = 10  # constant
    L = len_0 / max_dist  # len_0 - length of side of display square area
    length = np.full((num_nodes, num_nodes), np.inf)
    strength = np.full((num_nodes, num_nodes), np.inf)

    for i in range(num_nodes):
        for j in range(num_nodes):
            if i != j:
                length[i, j] = L * distances[i, j]
                strength[i, j] = k / (distances[i, j] * distances[i, j])

    points = []
    for i in range(num_nodes):
        x = len_0 * random()
        y = len_0 * random()
        points.append((x, y))

    maxi, delta = generate_delta(num_nodes, points, strength, length)
    eps = 0.01

    plt.close()
    draw_fig(G, points)
    plt.savefig(f"kk_images/KK_0.png")

    c = 1

    while delta[maxi] > eps:
        while delta[maxi] > eps:
            pd_xx = 0
            pd_xy = 0
            pd_x = 0
            pd_y = 0
            pd_yy = 0

            for i in range(num_nodes):
                if i == maxi:
                    continue
                norm = math.sqrt((points[maxi][0] - points[i][0]) ** 2 + (points[maxi][1] - points[i][1]) ** 2)

                x_mi = points[maxi][0] - points[i][0]
                y_mi = points[maxi][1] - points[i][1]

                pd_x += strength[maxi][i] * x_mi * (1.0 - length[maxi][i] / norm)
                pd_y += strength[maxi][i] * y_mi * (1.0 - length[maxi][i] / norm)

                pd_xy += strength[maxi][i] * length[maxi][i] * x_mi * y_mi / (norm ** 3)
                pd_xx += strength[maxi][i] * (1.0 - length[maxi][i] * y_mi ** 2 / (norm ** 3))
                pd_yy += strength[maxi][i] * (1.0 - length[maxi][i] * x_mi ** 2 / (norm ** 3))

            determinant = pd_xx * pd_yy - pd_xy * pd_xy
            # Cramer's rule
            dx = -(pd_yy * pd_x - pd_xy * pd_y) / determinant
            dy = -(-pd_xy * pd_x + pd_xx * pd_y) / determinant

            points[maxi] += np.array([dx, dy])

            delta[maxi] = np.sqrt(pd_x * pd_x + pd_y * pd_y)

        maxi, delta = generate_delta(num_nodes, points, strength, length)
        if flag:
            plt.figure(figsize=(8, 6))
            nx.draw_networkx(G, pos=points, node_size=10, width=0.1, with_labels=False)
            plt.title('Kamada-Kawai Layout')
            plt.axis('off')
            plt.savefig(f"kk_images/{c}.png")
            plt.close()
            c = c+1

    plt.figure(figsize=(8, 6))
    nx.draw_networkx(G, points, node_size=10, width=0.1, with_labels=False)
    plt.title('Kamada-Kawai Layout')
    plt.axis('off')
    plt.savefig("kk_images/final.png")
    plt.close()
