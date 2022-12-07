import networkx as nx
import matplotlib.pyplot as plt

import config


class Graph:
    def __init__(self):
        """Initialize grapher by making a directed graph"""
        self.G = nx.DiGraph()

    def populate_graph(self, data):
        """Populate G with the edges and weights"""
        for state, transitions in data.items():
            for transition, cost in transitions:
                self.G.add_edge(state, transition, weight=cost)

    def make_graph(self):
        """Create the graph visualization. X-forwarding is required to function."""
        # Networkx plotting
        # Planar layout seems to work the best in general
        pos = nx.planar_layout(self.G)
        nx.draw_networkx_nodes(self.G, pos, node_size=500)
        nx.draw_networkx_labels(self.G, pos)
        nx.draw_networkx_edges(self.G, pos)
        elabels = nx.get_edge_attributes(self.G, "weight")
        nx.draw_networkx_edge_labels(self.G, pos, elabels)

        if config.save_graph:
            plt.savefig("graph.png")
        if config.display_graph:
            plt.show()

    def path_analysis(self):
        # Get all the simple paths from G going from the initial state to the end state
        paths = list(nx.all_simple_paths(
            self.G, source=config.init_state, target=config.end_state))
        index = 1
        for path in paths:
            print("PATH " + str(index) + ": ", end="")
            self.fprint(path)
            index += 1

        # Several checks to do
        # Uneven states visited
        # Uneven computation time
        # If uneven computation time and states are even, find the problem state transitions
        for i in range(0, len(paths)):
            for j in range(i + 1, len(paths)):
                path1 = paths[i]
                path2 = paths[j]
                p1w = nx.path_weight(self.G, path1, "weight")
                p2w = nx.path_weight(self.G, path2, "weight")
                if len(path1) != len(path2):
                    print("LOW: uneven state transitions between paths " +
                          str(i+1) + " and " + str(j+1))
                if p1w != p2w:
                    print("HIGH: different computation timings between paths " + str(i+1) +
                          " (" + str(p1w) + ")" + " and " + str(j+1) + " (" + str(p2w) + ")")

    def fprint(self, path):
        l = len(path) - 1
        i = 0
        for state in path:
            if i == l:
                print(state)
                break
            print(state + "->", end="")
            i += 1
