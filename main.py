import matplotlib.pyplot as plt
import networkx as nx

from fruchterman_reingold import fruchterman_reingold
from kamada_kawai import kk_layout
from force_atlas import force_atlas_layout

def main():
    #G = nx.cubical_graph()
    G = nx.karate_club_graph()
    fruchterman_reingold(G)
    force_atlas_layout(G, gravity = 1.0)
    plt.close()
    nx.draw_networkx(G, pos=nx.kamada_kawai_layout(G), node_size=10, width=0.1, with_labels=False)
    plt.savefig("nx_kk.png")
    plt.close()
    nx.draw_networkx(G, pos=nx.spring_layout(G), node_size=10, width=0.1, with_labels=False)
    plt.savefig("nx_fr.png")
    kk_layout(G)

if __name__ == "__main__":
    main()
