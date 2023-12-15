import matplotlib.pyplot as plt
import networkx as nx

from force_atlas import force_atlas_layout
from fruchterman_reingold import fruchterman_reingold
from kamada_kawai import kk_layout


def main():
    try:
        G = nx.cubical_graph()
        print(f"Number of nodes: {nx.number_of_nodes(G)}")
        plt.close()
        nx.draw_networkx(G, pos=nx.kamada_kawai_layout(G), node_size=10, width=0.1, with_labels=False)
        plt.savefig("nx_kk.png")
        plt.close()
        nx.draw_networkx(G, pos=nx.spring_layout(G), node_size=10, width=0.1, with_labels=False)
        plt.savefig("nx_fr.png")
        input_num = int(input("Enter a choice: 1 for FR, 2 for KK, 3 for FA, 0 to exit:  "))
        # flag = bool(input("Do you want to print the images:(True or False)  "))
        while input_num != 0:
            if input_num == 1:
                iterations = int(input("Enter number of iterations "))
                fruchterman_reingold(G, iterations, True)
            elif input_num == 2:
                kk_layout(G, True)
            elif input_num == 3:
                iterations = int(input("Enter number of iterations "))
                force_atlas_layout(G, iterations=iterations, gravity=1.0, flag=True)
            input_num = int(input("Enter a choice: 1 for FR, 2 for KK, 3 for FA, 0 to exit:  "))

    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    main()
