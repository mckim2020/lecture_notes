import argparse
from graph_utils import *
from latex_utils import *



""" Receive Arguments """
parser = argparse.ArgumentParser()
parser.add_argument('--n_nodes', type=int, default=4, help="Number of nodes of graphs")
args = parser.parse_args()



""" Play with graphs """
# Generate all graphs
n_nodes = args.n_nodes
assert n_nodes > 1, "Number of nodes must be greater than 1"
n_node_graphs = [g for g in graph_atlas_g() if len(g.nodes())==n_nodes]
print("Total number of graphs:", len(n_node_graphs))

# Sort out connected graphs
n_node_graphs_connected = []
for graph in n_node_graphs:
    if nx.is_connected(graph):
        n_node_graphs_connected.append(graph)
print("Total number of connected graphs:", len(n_node_graphs_connected))

# Sort out 2-connected graphs
n_node_graphs_2_connected = []
for graph in n_node_graphs_connected:
    if is_2_connected(graph):
        n_node_graphs_2_connected.append(graph)
print("Total number of 2-connected graphs:", len(n_node_graphs_2_connected))

# Obtain degree of freedom of each graph
unique_adjs_list = []
for i, graph in enumerate(n_node_graphs_2_connected):
    unique_adjs = get_unique_adjs(graph)
    unique_adjs_list.append(unique_adjs)
    print(f"Graph {i+1} has degree of freedom {len(unique_adjs)}")
n_dofs = [len(unique_adjs) for unique_adjs in unique_adjs_list]

# Plot results
plot_graphs(n_node_graphs, save_dir='n_node_graphs')
plot_graphs(n_node_graphs_connected, save_dir='n_node_graphs_connected')
plot_graphs(n_node_graphs_2_connected, n_dofs, save_dir='n_node_graphs_2_connected')



""" Generate expressions """
vir_expr = gen_expr(unique_adjs_list, n_dofs)
latex_expr = latexify_expr(vir_expr, n_nodes=n_nodes)
plot_latex_expr(latex_expr)
print("LaTeX expression of the virial coefficient:")
print(latex_expr)



# Print out Latex expression of Virial coefficient
from IPython.display import Math, display
vir_expr = gen_expr(unique_adjs_list, n_dofs)
latex_expr = latexify_expr(vir_expr, n_nodes)
display(Math(latex_expr))