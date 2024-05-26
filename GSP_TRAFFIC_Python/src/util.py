import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from scipy.sparse import find
from typing import List
from pathlib import Path
from pygsp import filters


def top_dir() -> Path:
    return Path(__file__).parent.parent


def draw_graph(
    G,
    pos: np.ndarray,
    data: np.ndarray = None,
    image: str = None,
    fig_title: str = None,
    use_node_values: np.ndarray = None,
    node_value_disabled: bool = False,
):
    position_dict = {
        node_num: (pos_x, pos_y) for node_num, (pos_x, pos_y) in enumerate(pos)
    }
    node_value_disabled = _check_node_value_disabled(
        data, use_node_values, node_value_disabled
    )
    if not node_value_disabled and use_node_values is None:
        use_node_values = data
    node_sizes = _make_node_size(data, node_value_disabled)
    edges = _make_edge(G)
    graphD = _make_graphD(G=G, edges=edges)
    _save_graph(
        graphD=graphD,
        use_node_values=use_node_values,
        node_sizes=node_sizes,
        position_dict=position_dict,
        save_image_name=image,
        fig_title=fig_title,
        node_value_disabled=node_value_disabled,
    )


def _check_node_value_disabled(data, use_node_values, node_value_disabled) -> bool:
    if node_value_disabled:
        return node_value_disabled
    node_value_disabled = data is None and use_node_values is None
    if data is None and use_node_values is not None:
        raise Exception("Please input `data` into draw_graph to show the node values.")
    return node_value_disabled


def _make_edge(G) -> List:
    W = find(G.W)
    edge_len = len(W[0])
    edges = [[int(W[0][i]), int(W[1][i])] for i in range(edge_len)]
    return edges


def _make_graphD(G, edges: List) -> nx.DiGraph | nx.Graph:
    if G.is_directed():
        graphD = nx.DiGraph()
    else:
        graphD = nx.Graph()
    graphD.add_edges_from(edges)
    return graphD


def _make_node_size(data: np.ndarray, node_value_disabled: bool) -> List:
    if node_value_disabled:
        node_sizes = 10
    else:
        mean_data = sum(data) / len(data)
        node_sizes = [20 * float(signal / mean_data) for signal in data]
    return node_sizes


def _save_graph(
    graphD: nx.DiGraph | nx.Graph,
    use_node_values: np.ndarray,
    node_sizes: List[float],
    position_dict: dict,
    save_image_name: str,
    fig_title: str,
    node_value_disabled: bool,
) -> None:
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(1, 1, 1)
    if node_value_disabled:
        nx.draw_networkx_nodes(G=graphD, pos=position_dict, node_size=node_sizes)
    else:
        nx.draw_networkx_nodes(
            G=graphD,
            pos=position_dict,
            node_color=use_node_values,
            cmap="turbo",
            node_size=node_sizes,
        )
        sm = plt.cm.ScalarMappable(
            cmap="turbo",
            norm=plt.Normalize(vmin=min(use_node_values), vmax=max(use_node_values)),
        )
        sm.set_array([0, max(use_node_values)])
        fig.colorbar(sm, ax=ax)
    nx.draw_networkx_edges(G=graphD, pos=position_dict, width=0.2)
    if fig_title:
        ax.set_title(fig_title)
    fig.tight_layout()
    if isinstance(save_image_name, str):
        save_path = top_dir() / save_image_name
        fig.savefig(save_path, dpi=500)
    plt.close(fig)


def apply_gft_to_signal(G, graph_signal: np.ndarray):
    G.compute_fourier_basis()
    gft_signal = G.gft(graph_signal)
    return gft_signal


def save_gs_spectrum(
    gft_signal: np.ndarray, save_image_name: str, fig_title: str = None
):
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(1, 1, 1)
    signal_index = [i for i in range(len(gft_signal))]
    ax.stem(signal_index, np.abs(gft_signal))
    if fig_title:
        ax.set_title(fig_title)
    fig.tight_layout()
    if isinstance(save_image_name, str):
        save_path = top_dir() / save_image_name
        fig.savefig(save_path, dpi=500)
    plt.close(fig)


def normalize_graph_signal(graph_signal: np.ndarray, axis: int = 0) -> np.ndarray:
    mean_gs = np.mean(graph_signal, axis=axis, keepdims=True)
    std_gs = np.std(graph_signal, axis=axis, keepdims=True)
    return (graph_signal - mean_gs) / std_gs


def gsp_design_smooth_indicator(G, a1, a2):
    G.compute_fourier_basis()
    lmax = G.lmax
    fx = lambda x, a: np.exp(-a / x) * (x >= 0)
    gx = lambda x, a: fx(x, a) / (fx(x, a) + fx(1 - x, a))
    ffin = lambda x, a1, a2: gx(1 - (x - a1) / (a2 - a1), 1) * (x >= a1)
    g = lambda x: ffin(x / lmax, a1, a2)
    return filters.Filter(G, g)


def save_filter(g, filter_name: str, fig_title: str = None):
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(1, 1, 1)
    g.plot(plot_eigenvalues=True, ax=ax)
    if fig_title:
        ax.set_title(fig_title)
    save_path = top_dir() / filter_name
    fig.tight_layout()
    plt.savefig(save_path)
