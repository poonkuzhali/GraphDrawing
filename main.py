import matplotlib.pyplot as plt
import networkx as nx

from fruchterman_reingold import fruchterman_reingold
from kamada_kawai import kk_layout
from force_atlas import force_atlas_layout

def main():
    G = nx.cubical_graph()
    #G = nx.barbell_graph(6, 5)
    #G = nx.full_rary_tree(2,2)
    #G = nx.karate_club_graph()
    #G = nx.circular_ladder_graph(10)
    #G = nx.dorogovtsev_goltsev_mendes_graph(5, create_using=None)
    #G = nx.paley_graph(37)
    #G = nx.hexagonal_lattice_graph(2,2)
    #G = nx.triangular_lattice_graph(5,5)
    #G = nx.krackhardt_kite_graph()
    #G = nx.moebius_kantor_graph()
    #G = nx.tutte_graph()

    fruchterman_reingold(G)
    kk_layout(G)
    force_atlas_layout(G, gravity = 1.0, plot_iterations = 0)

    plt.close()
    nx.draw_networkx(G, pos=nx.kamada_kawai_layout(G), node_size=10, width=0.1, with_labels=False)
    plt.savefig("nx_kk.png")
    plt.close()
    nx.draw_networkx(G, pos=nx.spring_layout(G), node_size=10, width=0.1, with_labels=False)
    plt.savefig("nx_fr.png")

if __name__ == "__main__":
    main()
