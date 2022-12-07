import parser
import graph
import config

import sys


def main():
    pars = parser.Parser()
    grapher = graph.Graph()
    pars.read_file(config.verilog_source)
    pars.parse()
    grapher.populate_graph(pars.graph)
    grapher.path_analysis()

    # Only make the graph visual if option is chosen
    # NOTE: X-server MUST be properly configured and running to graph as part of
    # matplotlib requirements
    if config.display_graph or config.save_graph:
        grapher.make_graph()


if __name__ == "__main__":
    main()
