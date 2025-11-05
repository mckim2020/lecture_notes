import math
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
import matplotlib as mpl
# from sympy import symbols, Function, Add
from sympy.printing import latex
# import latexify



# @latexify.function
def gen_expr(unique_adjs_list, n_dofs):    
    expr = sp.Integer(0)
    for i, unique_adjs in enumerate(unique_adjs_list):
        # extract unique pairs of edges
        mask = np.tril(np.ones((unique_adjs.shape[1:3])), k=-1)
        unique_adjs[:, mask.astype(bool)] = 0
        indices = np.argwhere(unique_adjs == 1)[:, 1:]

        # group in terms
        n_dof = unique_adjs.shape[0]
        n_links = indices.shape[0] // n_dof
        sub_indices = indices[0:n_links]

        # update expression
        expr += n_dofs[i] * sp.Mul(*[sp.Function('f')(sp.Symbol(f'r_{{{min(pair)+1}{max(pair)+1}}}')) for pair in sub_indices])
        # expr += n_dofs[i] * sp.Mul(*[sp.Function('f')(sp.Symbol(f'r_{{{min(pair)+1}{max(pair)+1}}}')) for pair in sub_indices])
        # expr += n_dofs[i] \
            #   * sp.Mul(*[sp.Function('f')
                        #  (sp.Abs(sp.Symbol(f'r_{pair[0]+1}') - sp.Symbol(f'r_{pair[1]+1}'))) 
                        #  for pair in sub_indices])

    return expr

def latexify_expr(expr, n_nodes=4):
    """
    Convert a SymPy expression to LaTeX format and print it.
    """
    # If the expression is a sum, split it into terms
    if isinstance(expr, sp.Add): terms = expr.args
    else: terms = [expr]
    
    # Convert each term to LaTeX and join with newlines and plus signs
    latex_terms = [latex(term) for term in terms]

    if len(latex_terms) == 1:
        latex_expr = ''
        latex_expr += f'\mathcal{{B}}_{n_nodes} = ' 
        latex_expr += f'-\\frac{{1}}{{{n_nodes}V}} '
        for i in range(n_nodes): latex_expr += f'\int_V d^3r_{i+1} '
        latex_expr += '\,\,\,'
        latex_expr += latex_terms[0]

    elif len(latex_terms) > 1:
        latex_expr = ''
        latex_expr += f'\mathcal{{B}}_{n_nodes} = '
        latex_expr += f'-\\frac{{1}}{{{n_nodes}V}} '
        for i in range(n_nodes): latex_expr += f'\int_V d^3r_{i+1} '
        latex_expr += '\,\,\, '
        latex_expr += latex_terms[0]
        for term in latex_terms[1:]:
            latex_expr += f' + {term}'

    return latex_expr

def latexify_expr_new(expr, n_nodes=4):
    # if the expression is a sum, split it into terms
    if isinstance(expr, sp.Add): terms = expr.args
    else: terms = [expr]

    # convert each term to LaTeX and join with newlines and plus signs
    latex_terms = [sp.latex(term) for term in terms]

    if len(latex_terms) == 1:
        latex_expr = ''
        latex_expr += f'\mathcal{{B}}_{n_nodes} = '
        latex_expr += f'-\\frac{{1}}{{{n_nodes}V}} '
        for i in range(n_nodes): latex_expr += f'\int_V d^3r_{i+1} '
        latex_expr += '\,\,\,'
        latex_expr += latex_terms[0]

    elif len(latex_terms) > 1:
        latex_expr = ''
        # latex_expr = f'\\begin{{split}}'
        # latex_expr += '\\begin{align}'
        latex_expr += f'\mathcal{{B}}_{n_nodes} = '
        latex_expr += f'-\\frac{{1}}{{{n_nodes}V}} '
        for i in range(n_nodes): latex_expr += f'\int_V d^3r_{i+1}'
        latex_expr += '\,\,\, '
        latex_expr += '\\Big['
        latex_expr += latex_terms[0]
        for term in latex_terms[1:]:
            latex_expr += ' \\\\ ' + '\\hspace{' + str(3 * n_nodes + 7) + 'em}'  + f'+ {term}'
        # latex_expr += f'\\end{{split}}'
        latex_expr += '\\Big]'
        # latex_expr += '\\end{align}'

    return latex_expr

def plot_latex_expr(latex_expr):
    fig, ax = plt.subplots(figsize=(8, 2))  # Adjust size as needed
    ax.text(0.5, 0.5, rf'${latex_expr}$', fontsize=14, ha='center', va='center')

    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_frame_on(False)

    plt.savefig('latex_expr.png', bbox_inches='tight')
    plt.clf()