import math
from random import random
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np


def force_atlas_layout(G, iterations=200, gravity=1.0, flag=False):
    # initial positions of points
    # mass of nodes = degree of the nodes
    for v in nx.nodes(G):
        G.nodes[v]['x'] = random()
        G.nodes[v]['y'] = random()
        G.nodes[v]['mass'] = 1 + np.count_nonzero(G[v])
        G.nodes[v]['old_dx'] = 0
        G.nodes[v]['old_dy'] = 0
        G.nodes[v]['dx'] = 0
        G.nodes[v]['dy'] = 0

    speed = 1
    speed_efficiency = 1
    jitter_tolerance = 1.0
    pos = {}

    for i in range(0, iterations):
        # Reset iteration data
        for v in nx.nodes(G):
            G.nodes[v]['old_dx'] = G.nodes[v]['dx']
            G.nodes[v]['old_dy'] = G.nodes[v]['dy']
            G.nodes[v]['dx'] = 0
            G.nodes[v]['dy'] = 0
            # apply_repulsion - between nodes
        coefficient = 1
        for u in nx.nodes(G):
            for w in nx.nodes(G):
                if w != u:
                    x_dist = G.nodes[u]['x'] - G.nodes[w]['x']
                    y_dist = G.nodes[u]['y'] - G.nodes[w]['y']
                    distance2 = x_dist * x_dist + y_dist * y_dist  # Distance squared
                    if distance2 > 0:
                        factor = coefficient * G.nodes[w]["mass"] * G.nodes[u]["mass"] / distance2
                        G.nodes[u]['dx'] += x_dist * factor
                        G.nodes[u]['dy'] += y_dist * factor
        # apply_gravity - attract nodes to center
        for u in nx.nodes(G):
            x_dist = G.nodes[u]['x']
            y_dist = G.nodes[u]['y']
            distance = math.sqrt(x_dist ** 2 + y_dist ** 2)

            if distance > 0:
                factor = coefficient * G.nodes[u]["mass"] * gravity / distance
                G.nodes[u]['dx'] -= x_dist * factor
                G.nodes[u]['dy'] -= y_dist * factor
        # apply_attraction
        edge_weight = 1
        for v, u in G.edges():
            x_dist = G.nodes[v]['x'] - G.nodes[u]['x']
            y_dist = G.nodes[v]['y'] - G.nodes[u]['y']
            factor = -coefficient * edge_weight
            G.nodes[v]['dx'] += x_dist * factor
            G.nodes[v]['dy'] += y_dist * factor
            G.nodes[u]['dx'] -= x_dist * factor
            G.nodes[u]['dy'] -= y_dist * factor
        # Speed adjustment
        total_swinging = 0.0  # irregular movement
        total_effective_traction = 0.0  # useful movement
        for v in nx.nodes(G):
            old_dx = G.nodes[v]['old_dx']
            old_dy = G.nodes[v]['old_dy']
            dx = G.nodes[v]['dx']
            dy = G.nodes[v]['dy']
            mass = G.nodes[v]['mass']
            swinging = math.sqrt((old_dx - dx) * (old_dx - dx) + (old_dy - dy) * (old_dy - dy))
            total_swinging += mass * swinging
            total_effective_traction += .5 * mass * math.sqrt(
                (old_dx + dx) * (old_dx + dx) + (old_dy + dy) * (old_dy + dy))

        estimated_optimal_jitter_tolerance = .05 * math.sqrt(nx.number_of_nodes(G))
        min_jt = math.sqrt(estimated_optimal_jitter_tolerance)
        max_jt = 10
        jt = jitter_tolerance * max(min_jt, min(max_jt,
                                                estimated_optimal_jitter_tolerance * total_effective_traction / (
                                                        nx.number_of_nodes(G) ** 2)))

        min_speed_efficiency = 0.05

        # Update max jitter
        if total_swinging / total_effective_traction > 2.0:
            if speed_efficiency > min_speed_efficiency:
                speed_efficiency *= .5
            jt = max(jt, jitter_tolerance)

        target_speed = jt * speed_efficiency * total_effective_traction / total_swinging

        # update speed efficiency
        if total_swinging > jt * total_effective_traction:
            if speed_efficiency > min_speed_efficiency:
                speed_efficiency *= .7
        elif speed < 1000:
            speed_efficiency *= 1.3

        max_rise = .5
        speed = speed + min(target_speed - speed, max_rise * speed)

        # Update positions
        for v in nx.nodes(G):
            dx = G.nodes[v]['dx']
            dy = G.nodes[v]['dy']
            mass = G.nodes[v]['mass']
            old_dx = G.nodes[v]['old_dx']
            old_dy = G.nodes[v]['old_dy']
            swinging = mass * math.sqrt((old_dx - dx) * (old_dx - dx) + (old_dy - dy) * (old_dy - dy))
            factor = speed / (1.0 + math.sqrt(speed * swinging))
            G.nodes[v]['x'] += (dx * factor)
            G.nodes[v]['y'] += (dy * factor)

        for v in G.nodes():
            pos[v] = [G.nodes[v]['x'], G.nodes[v]['y']]

        if flag:
            plt.figure(figsize=(8, 6))
            nx.draw_networkx(G, pos, node_size=10, width=0.1, with_labels=False)
            plt.title('Force-Atlas Layout')
            plt.axis('off')
            plt.savefig("fa_images/{0}.png".format(i))
            plt.close()

    plt.figure(figsize=(8, 6))
    nx.draw_networkx(G, pos, node_size=10, width=0.1, with_labels=False)
    plt.title('Force-Atlas Layout')
    plt.axis('off')
    plt.savefig("fa_images/{0}.png".format(i))
    plt.close()
