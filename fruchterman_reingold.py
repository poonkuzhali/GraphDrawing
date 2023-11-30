import math
from random import random

import matplotlib.pyplot as plot
import networkx as nx


def attractive_force(d, k):
    return d * d / k


def repulsive_force(d, k):
    return k * k / d


def draw_fig(graph, positions):
    plot.figure(figsize=(8, 6))
    nx.draw_networkx(graph, pos=positions, node_size=10, width=0.1, with_labels=False)
    plot.title('Fruchterman-Reingold Layout')
    plot.axis('off')


def fruchterman_reingold(graph, iterations, flag):
    width = 1  # Width of the frame
    length = 1  # Length of the frame
    area = width * length
    k = math.sqrt(area / nx.number_of_nodes(graph))  # optimal distance between vertices
    iterations = iterations

    # Place nodes randomly in the layout
    for v in nx.nodes(graph):
        graph.nodes[v]['x'] = width * random()
        graph.nodes[v]['y'] = length * random()

    temperature = width / 10  # one tenth the width of the frame
    dt = temperature / iterations

    print("area:{0}".format(area))
    print("k:{0}".format(k))
    print("t:{0}, dt:{1}".format(temperature, dt))

    for i in range(iterations):
        print("iter {0}".format(i))

        # Draw initial layout
        positions = {}
        for v in graph.nodes():
            positions[v] = [graph.nodes[v]['x'], graph.nodes[v]['y']]
        if i == 0:
            plot.close()
            draw_fig(graph, positions)
            plot.savefig("fr_images/{0}.png".format(i))

        # Calculating repulsive forces
        for v in graph.nodes():
            # displacement of the vector
            graph.nodes[v]['dx'] = 0
            graph.nodes[v]['dy'] = 0
            for u in graph.nodes():
                if v != u:
                    # Calculating difference between the position of two vertices (ie) v.pos - u.pos
                    dx = graph.nodes[v]['x'] - graph.nodes[u]['x']
                    dy = graph.nodes[v]['y'] - graph.nodes[u]['y']
                    # Delta is the difference vector between the position of two vertices
                    delta = math.sqrt(dx * dx + dy * dy)
                    if delta != 0:
                        rep_force = repulsive_force(delta, k) / delta
                        graph.nodes[v]['dx'] += dx * rep_force
                        graph.nodes[v]['dy'] += dy * rep_force

        # Calculating attractive forces
        for v, u in graph.edges():
            dx = graph.nodes[v]['x'] - graph.nodes[u]['x']
            dy = graph.nodes[v]['y'] - graph.nodes[u]['y']
            delta = math.sqrt(dx * dx + dy * dy)
            if delta != 0:
                d = attractive_force(delta, k) / delta
                graph.nodes[v]['dx'] = graph.nodes[v]['dx'] - dx * d
                graph.nodes[u]['dx'] = graph.nodes[u]['dx'] + dx * d
                graph.nodes[v]['dy'] = graph.nodes[v]['dy'] - dy * d
                graph.nodes[u]['dy'] = graph.nodes[u]['dy'] + dy * d

        # Limit max displacement to temperature and prevent from displacement outside frame
        for v in graph.nodes():
            dx = graph.nodes[v]['dx']
            dy = graph.nodes[v]['dy']
            disp = math.sqrt(dx * dx + dy * dy)
            if disp != 0:
                d = min(disp, temperature) / disp
                x = graph.nodes[v]['x'] + dx * d
                y = graph.nodes[v]['y'] + dy * d
                x = min(width, max(0, x)) - width / 2
                y = min(length, max(0, y)) - length / 2
                graph.nodes[v]['x'] = min(math.sqrt(width * width / 4 - y * y),
                                          max(-math.sqrt(width * width / 4 - y * y), x)) + width / 2
                graph.nodes[v]['y'] = min(math.sqrt(length * length / 4 - x * x),
                                          max(-math.sqrt(length * length / 4 - x * x), y)) + length / 2

        # cooling
        temperature -= dt
        if flag:
            plot.close()
            draw_fig(graph, positions)
            plot.savefig("fr_images/{0}.png".format(i))

    positions = {}
    for v in graph.nodes():
        positions[v] = [graph.nodes[v]['x'], graph.nodes[v]['y']]
    plot.close()
    draw_fig(graph, positions)
    plot.savefig("fr_images/Final_FR")

    return positions
