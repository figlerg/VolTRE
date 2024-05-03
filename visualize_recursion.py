import os

import networkx as nx
import matplotlib.pyplot as plt
from antlr4 import *
from parse.TRELexer import TRELexer
from parse.TREParser import TREParser
from os.path import join

import matplotlib.pyplot as plt
import networkx as nx
import pydot
from networkx.drawing.nx_pydot import graphviz_layout

# Function to generate syntax tree graph
def generate_syntax_tree(ctx, graph=None, parent_node=None):
    if graph is None:
        graph = nx.DiGraph()

    if isinstance(ctx, TerminalNode):
        # Handle terminal (leaf) nodes
        pass
    else:
        # Handle non-terminal (internal) nodes
        node = str(ctx)
        label_text = ctx.getText()
        graph.add_node(node, label=label_text)

        if parent_node:
            graph.add_edge(parent_node, node)
        if isinstance(ctx, TREParser.AtomicExprContext):
            return graph  # otherwise we get annoying repeat of the node
        for child in ctx.children:
            generate_syntax_tree(child, graph, node)

    return graph

# Parse the input and generate syntax tree
input_stream = FileStream(join('parse', 'test.txt'))
lexer = TRELexer(input_stream)
stream = CommonTokenStream(lexer)
parser = TREParser(stream)
ctx = parser.expr()

# Generate the syntax tree graph
G = generate_syntax_tree(ctx)

# Draw the graph
# pos = graphviz_layout(G, prog="dot")
# nx.draw(G, pos, with_labels=True, labels=nx.get_node_attributes(G, 'label'), node_color='none', edge_color='black', node_size=100, font_size=12, font_color='black', linewidths=1, edgecolors='black', bbox=dict(facecolor="white"))
# plt.show()




def highlight_node(G:nx.DiGraph, node, n):
    # assert(node in G.nodes), "trying to highlight a non-existing node"

    # Draw the graph
    pos = graphviz_layout(G, prog="dot")
    # nx.draw(G, pos, with_labels=True, labels=nx.get_node_attributes(G, 'label'), node_color='none', edge_color='black',
    #         node_size=100, font_size=12, font_color='black',  linewidths=1, edgecolors='black',
    #         bbox=dict(facecolor="white"))
    cs = []
    for v in G.nodes.keys():
        c = 'none' if v != node else 'red'
        cs.append(c)

    labels = nx.get_node_attributes(G, 'label').copy()
    labels[node] += f"     n = {n}"

    nx.draw(G, pos, with_labels=True, labels=labels, node_color = cs)
    # plt.show()
    vis_dir_path = os.path.join(os.curdir, 'vis_cache')
    file_n = len([name for name in os.listdir(vis_dir_path) if os.path.isfile(os.path.join(vis_dir_path,name))]) + 1
    file_path = os.path.join(vis_dir_path, f"file{file_n}.png")
    plt.savefig(file_path)
    plt.clf()


if __name__ == '__main__':

    node = next(G.nodes.keys().__iter__())

    highlight_node(G,node, 3)

