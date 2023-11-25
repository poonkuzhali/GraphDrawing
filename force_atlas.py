import math
from random import random
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

def force_atlas_layout(G,
                        iterations=100,
                        gravity=1.0,
                        repulsion_coefficient = 1.0,
                        speed_tolerance = 1.0,
                        ks = 0.1,
                        ksmax = 10,
                        plot_iterations = 0
                        ):

    #initial positions of points
    #mass of nodes = degree of the nodes
    for v in nx.nodes(G):
        G.nodes[v]['x'] = random()
        G.nodes[v]['y'] = random()
        G.nodes[v]['mass'] = np.count_nonzero(G[v])
        G.nodes[v]['old_dx'] = 0
        G.nodes[v]['old_dy'] = 0
        G.nodes[v]['dx'] = 0
        G.nodes[v]['dy'] = 0

    #Start Force Atlas 2 Algorithm iterations
    for i in range (0, iterations):
        print("fa iter {0}".format(i))

        #Reset iteration data
        for v in nx.nodes(G):
            G.nodes[v]['old_dx'] = G.nodes[v]['dx']
            G.nodes[v]['old_dy'] = G.nodes[v]['dy']
            G.nodes[v]['dx'] = 0
            G.nodes[v]['dy'] = 0        
        
        #apply_repulsion - between nodes
        for u in nx.nodes(G):
            for w in nx.nodes(G):
                if w != u:
                    x_dist = G.nodes[u]['x'] - G.nodes[w]['x']
                    y_dist = G.nodes[u]['y'] - G.nodes[w]['y']
                    distance2 = x_dist ** 2 + y_dist ** 2  # Distance squared
                    if distance2 > 0:
                        factor = repulsion_coefficient * G.nodes[w]["mass"] * G.nodes[u]["mass"] / distance2
                        G.nodes[u]['dx'] += x_dist * factor
                        G.nodes[u]['dy'] += y_dist * factor
        
        #apply_gravity - attract nodes to center
        for u in nx.nodes(G):
            x_dist = G.nodes[u]['x']
            y_dist = G.nodes[u]['y']
            distance = math.sqrt(x_dist ** 2 + y_dist ** 2)
            if distance > 0:
                factor = G.nodes[u]["mass"] * gravity / distance
                G.nodes[u]['dx'] -= x_dist * factor
                G.nodes[u]['dy'] -= y_dist * factor

        #apply_attraction - between edges
        edge_weight = 1
        for v, u in G.edges():
            x_dist = G.nodes[v]['x'] - G.nodes[u]['x']
            y_dist = G.nodes[v]['y'] - G.nodes[u]['y']
            factor = - edge_weight
            G.nodes[v]['dx'] += x_dist * factor
            G.nodes[v]['dy'] += y_dist * factor
            G.nodes[u]['dx'] -= x_dist * factor
            G.nodes[u]['dy'] -= y_dist * factor

        #Speed adjustment
        total_swinging = 0.0            # erratic movement
        total_effective_traction = 0.0  # useful movement
        for v in nx.nodes(G):
            old_dx = G.nodes[v]['old_dx'] 
            old_dy = G.nodes[v]['old_dy'] 
            dx = G.nodes[v]['dx']
            dy = G.nodes[v]['dy']
            mass = G.nodes[v]['mass']
            swinging = math.sqrt((old_dx - dx) * (old_dx - dx) + (old_dy - dy) * (old_dy - dy))
            total_swinging += mass * swinging
            total_effective_traction += .5 * mass * math.sqrt((old_dx + dx) * (old_dx + dx) + (old_dy + dy) * (old_dy + dy))

        global_speed = speed_tolerance * total_effective_traction / total_swinging

        # Update positions
        for v in nx.nodes(G):
            dx = G.nodes[v]['dx']
            dy = G.nodes[v]['dy']
            mass = G.nodes[v]['mass']
            old_dx = G.nodes[v]['old_dx'] 
            old_dy = G.nodes[v]['old_dy'] 
            swinging = mass * math.sqrt((old_dx - dx) * (old_dx - dx) + (old_dy - dy) * (old_dy - dy))
            max_speed = ksmax / math.sqrt(dx ** 2 + dy ** 2)
            speed = ks * global_speed / ( 1.0 + global_speed * math.sqrt(swinging))
            factor = min(speed, max_speed) 
            G.nodes[v]['x'] += (dx * factor)
            G.nodes[v]['y'] += (dy * factor)

        #Plot graphs per iteration if set
        if plot_iterations:
            pos = {}
            for v in G.nodes():
                pos[v] = [G.nodes[v]['x'], G.nodes[v]['y']]

            plt.figure(figsize=(8, 6))
            nx.draw_networkx(G, pos, node_size=10, width=0.1, with_labels=False)
            plt.axis('off')
            plt.savefig("fa_{0}.png".format(i))
            plt.close()

    pos = {}
    for v in G.nodes():
        pos[v] = [G.nodes[v]['x'], G.nodes[v]['y']]

    plt.figure(figsize=(8, 6))
    nx.draw_networkx(G, pos, node_size=10, width=0.1, with_labels=False)
    plt.title('Force-Atlas 2 Layout')
    plt.axis('off')
    plt.savefig("force_atlas2.png")
    plt.close()
    
    return pos
