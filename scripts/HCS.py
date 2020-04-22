#!/u1/home/dc1321/anaconda3/bin/python3.7

"""
Implementation of Highly Connected Subgraphs (HCS) clustering,
Hartuv, E., & Shamir, R. (2000).  "A clustering algorithm based on graph connectivity". Information processing letters,
 76(4-6), 175-18
Using NetworkX and Numpy
Notation:
    G = Graph
    E = Edge
    V = Vertex
    |V| = Number of Vertices in G
    |E| = Number of Edges in G
works only with NetworkX 2.3 (not 2.4 for now)
"""

import itertools as itts
from pathlib import Path
from optparse import OptionParser, OptionValueError
import networkx as nx

def _check_inputFile(option, opt_str, value, parser):
    f_path = Path(value)
    if not f_path.is_file():
        raise OptionValueError(f"Cannot get {str(f_path)} file")
    setattr(parser.values, option.dest, Path(f_path))
    parser.values.saved_infile = True


def remove_edges(G, E):
    for edge in E:
        G.remove_edge(*edge)
    return G


def HCS_(G):

    def highly_connected(G, E):
        return len(E) >= len(G.nodes) / 2

    E = nx.algorithms.connectivity.cuts.minimum_edge_cut(G)
    if not highly_connected(G, E):
        G = remove_edges(G, E)
        sub_graphs = list(nx.connected_component_subgraphs(G))
        if len(sub_graphs) == 2:
            H1 = HCS_(sub_graphs[0])
            H2 = HCS_(sub_graphs[1])
            G = nx.compose(H1, H2)
    return G


def HCS(G):
    graph_list = []
    for g in nx.connected_component_subgraphs(G):
        if len(g) <= 2:
            graph_list.append(g)
        else:
            graph_list.append(HCS_(g))
    gr = nx.union_all(sorted(graph_list, key=lambda x: len(x), reverse=True))
    return gr


def read_data(inFile, num_lines: int = None):
    out_dict = {}
    with open(inFile) as oF:
        for ix, line in enumerate(itts.islice(oF, 0, num_lines)):
            line = line.strip()
            try:
                domain1, domain2, tm = line.split()
            except ValueError:
                print(f'wrong line {ix}')
                continue
            value = float(tm)
            if domain1 == domain2:
                continue
            if domain1 not in out_dict:
                out_dict[domain1] = {}
            out_dict[domain1][domain2] = dict(value=value)
    return out_dict


def make_graph(data_dict, cutoff=0.6):
    G = nx.Graph()
    nodes = [(n, dict(uid=n, label=n)) for n in data_dict.keys()]
    G.add_nodes_from(nodes)
    for node, v in data_dict.items():
        edges = [(node, x) for x in filter(
            lambda x: x in data_dict.keys(),  v.keys()) if v[x]['value'] <= cutoff]
        G.add_edges_from(edges)
    return G


def num_nodes(x):
    return(nx.number_of_nodes(x))


if __name__ == "__main__":
    options_parser = OptionParser()
    options_parser.add_option("-i", "--input_file",
                              dest="input_file", type='str',
                              help="input FILE",
                              metavar="FILE",
                              action='callback',
                              callback=_check_inputFile)
    options_parser.add_option("-o", "--out_file",
                              dest="out_file", type='str',
                              help="output FILE",
                              metavar="FILE")
    options_parser.add_option("-c", "--cutoff",
                              dest="cutoff", type='float',
                              help="clustering cutoff",
                              metavar="FLOAT")
    options_parser.add_option("-g", "--graph",
                              action="store_true",
                              dest="graph", default=False,
                              help="saves graphs in graphml format")
    (options, args) = options_parser.parse_args()
    in_file = Path(options.input_file)
    out_file = Path(options.out_file)
    cutoff = float(options.cutoff)
    start_graph_file = out_file.parent/f"{out_file.stem}_start.graphml"
    end_graph_file = out_file.parent/f"{out_file.stem}_end.graphml"

    data = read_data(in_file)

    G = make_graph(data, cutoff)
    oF = open(out_file, 'w')
    oF.write(f"# number nodes = {num_nodes(G)}\n")
    oF.write(f"# number edges = {nx.number_of_edges(G)}\n")

    if options.graph:
        nx.write_graphml(G, str(start_graph_file))
    G_HCS = HCS(G)
    if options.graph:
        nx.write_graphml(G, str(end_graph_file))
    # transitivity or connectivity in a graph,
    # Compute graph transitivity, the fraction of all possible triangles present in Graph #
    oF.write(f"transitivity {nx.transitivity(G_HCS)}\n")
    for ix, g in enumerate(
            nx.connected_component_subgraphs(G_HCS),  1):
        str_out = ""
        str_out += f"{ix} {num_nodes(g)}"
        for node, data in g.nodes.items():
            str_out += f" {data['label']}"
        oF.write(str_out+'\n')
    oF.write(f"# total cluster {ix}\n")
    oF.close()
