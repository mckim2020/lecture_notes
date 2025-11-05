import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from networkx import graph_atlas_g
from networkx.algorithms import isomorphism
from itertools import permutations



def create_grid_pos(n):
    grid_size = np.ceil(np.sqrt(n))
    pos = {}
    for i in range(n):
        row = i // grid_size
        col = i % grid_size
        pos[i] = (col / (grid_size - 1), 1 - row / (grid_size - 1))
    return pos

def plot_graphs(n_node_graphs, n_dofs=None, save_dir='graphs'):
    # set up the plot
    n_graphs = len(n_node_graphs)
    n_cols = 4 # may change
    n_rows = (n_graphs - 1) // n_cols + 1

    # plot graphs
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 4 * n_rows))
    axes = axes.flatten()

    for i, g in enumerate(n_node_graphs):
        ax = axes[i]

        grid_pos = create_grid_pos(len(g.nodes()))

        nx.draw(g, grid_pos, ax=ax, with_labels=True, node_color='lightblue',
                node_size=500, font_size=10, font_weight='bold')

        ax.set_title(f'Graph {i+1}')
        if n_dofs is not None: 
            ax.text(0.5, -0.1, f'DOF: {n_dofs[i]}', 
                    horizontalalignment='center', 
                    transform=ax.transAxes)

        ax.set_axis_off()

    for j in range(i+1, len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout()
    plt.savefig(f"{save_dir}.png")
    plt.clf()

# Sort out connected graphs
def is_connected(graph):
    """
    Sort out connected graphs
    """
    return nx.is_connected(graph)

def is_2_connected(graph):
    """
    Sort out 2-connected graphs
    """
    for node in list(graph.nodes()):
        # remove node
        temp_graph = graph.copy()
        temp_graph.remove_node(node)

        # connection check
        if nx.is_connected(temp_graph) == False:
          return False

    return True

def get_unique_adjs(graph):
    adj = nx.adjacency_matrix(graph).todense()
    n_nodes = adj.shape[0]
    unique_matrices = set()
    
    for perm in list(permutations(range(n_nodes))):
        perm_matrix = np.zeros((n_nodes, n_nodes))
        for i, j in enumerate(perm):
            perm_matrix[i, j] = 1

        multiplied_matrix = perm_matrix @ adj @ perm_matrix.T
        matrix_tuple = tuple(map(tuple, multiplied_matrix))
        unique_matrices.add(matrix_tuple)
    
    return np.array(list(unique_matrices))