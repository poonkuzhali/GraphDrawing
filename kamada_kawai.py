import math
from random import random

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np


def calc_Delta(n, points, k, l):
    max_delta = 0
    maxi = 0
    Delta = [0] * n
    for i in range(n):
        ex = 0
        ey = 0
        for j in range(n):
            if j == i:
                continue
            norm = math.sqrt((points[i][0] - points[j][0]) ** 2 + (points[i][1] - points[j][1]) ** 2)
            dxij = points[i][0] - points[j][0]
            dyij = points[i][1] - points[j][1]

            ex += k[i, j] * dxij * (1.0 - l[i, j] / norm)
            ey += k[i, j] * dyij * (1.0 - l[i, j] / norm)

        Delta[i] = math.sqrt(ex ** 2 + ey ** 2)
        if Delta[i] > max_delta:
            max_delta = Delta[i]
            maxi = i

    return maxi, Delta


def kk_layout(G):
    distances = np.array(nx.floyd_warshall_numpy(G, nodelist=G.nodes()))
    num_nodes = len(G.nodes())
    max_dist = 0
    for i in range(num_nodes):
        for j in range(num_nodes):
            if max_dist < distances[i, j]:
                max_dist = distances[i, j]

    L_zero = 1
    K = 10
    L = L_zero / max_dist
    l = np.full((num_nodes, num_nodes), np.inf)
    k = np.full((num_nodes, num_nodes), np.inf)

    for i in range(num_nodes):
        for j in range(num_nodes):
            if i != j:
                l[i, j] = L * distances[i, j]
                k[i, j] = K / (distances[i, j] * distances[i, j])

    points = []
    for i in range(num_nodes):
        x = L_zero * random()
        y = L_zero * random()
        points.append((x, y))

    maxi, Delta = calc_Delta(num_nodes, points, k, l)
    eps = 1.e-2

    while Delta[maxi] > eps:
        while Delta[maxi] > eps:
            Exx = 0
            Exy = 0
            Ex = 0
            Ey = 0
            Eyy = 0

            for i in range(num_nodes):
                if i == maxi:
                    continue
                norm = math.sqrt((points[maxi][0] - points[i][0]) ** 2 + (points[maxi][1] - points[i][1]) ** 2)

                dxmi = points[maxi][0] - points[i][0]
                dymi = points[maxi][1] - points[i][1]

                Ex += k[maxi][i] * dxmi * (1.0 - l[maxi][i] / norm)
                Ey += k[maxi][i] * dymi * (1.0 - l[maxi][i] / norm)

                Exy += k[maxi][i] * l[maxi][i] * dxmi * dymi / (norm ** 3)
                Exx += k[maxi][i] * (1.0 - l[maxi][i] * dymi ** 2 / (norm ** 3))
                Eyy += k[maxi][i] * (1.0 - l[maxi][i] * dxmi ** 2 / (norm ** 3))

            D = Exx * Eyy - Exy * Exy
            dx = -(Eyy * Ex - Exy * Ey) / D
            dy = -(-Exy * Ex + Exx * Ey) / D

            points[maxi] += np.array([dx, dy])

            Delta[maxi] = np.sqrt(Ex * Ex + Ey * Ey)
        maxi, Delta = calc_Delta(num_nodes, points, k, l)

    plt.figure(figsize=(8, 6))
    nx.draw(G, pos=points)
    plt.title('Kamada-Kawai Layout')
    plt.axis('off')
    plt.savefig("kamada.png")

