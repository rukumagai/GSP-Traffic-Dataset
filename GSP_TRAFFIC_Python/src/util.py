import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from scipy.sparse import find
from typing import List
from pathlib import Path


def top_dir() -> Path:
    return Path(__file__).parent.parent


def draw_graph(
    G,
    pos: np.ndarray,
    data: np.ndarray = None,
    image: str = None,
    use_node_values: np.ndarray = None,
):
    position_dict = {
        node_num: (pos_x, pos_y) for node_num, (pos_x, pos_y) in enumerate(pos)
    }
    if use_node_values is None:
        use_node_values = data
    node_sizes = _make_node_size(data)
    edges = _make_edge(G)
    graphD = _make_graphD(G=G, edges=edges)
    _save_graph(
        graphD=graphD,
        use_node_values=use_node_values,
        node_sizes=node_sizes,
        position_dict=position_dict,
        save_image_name=image,
    )


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


def _make_node_size(data: np.ndarray) -> List:
    if data is None:
        return None
    mean_data = sum(data) / len(data)
    node_sizes = [20 * float(signal / mean_data) for signal in data]
    return node_sizes


def _save_graph(
    graphD: nx.DiGraph | nx.Graph,
    use_node_values: np.ndarray,
    node_sizes: List[float],
    position_dict: dict,
    save_image_name: str,
) -> None:
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(1, 1, 1)
    if use_node_values is None:
        nx.draw_networkx_nodes(G=graphD, pos=position_dict, node_size=10)
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
    print(type(save_image_name))
    if isinstance(save_image_name, str):
        save_path = top_dir() / save_image_name
        fig.savefig(save_path, dpi=500)
    plt.close(fig)


def apply_gft_to_signal(G, graph_signal: np.ndarray):
    G.compute_fourier_basis()
    gft_signal = G.gft(graph_signal)
    return gft_signal


def save_gs_spectrum(gft_signal: np.ndarray, save_image_name: str):
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(1, 1, 1)
    signal_index = [i for i in range(len(gft_signal))]
    ax.stem(signal_index, np.abs(gft_signal))
    if isinstance(save_image_name, str):
        save_path = top_dir() / save_image_name
        fig.savefig(save_path, dpi=500)
    plt.close(fig)


def normalize_graph_signal(graph_signal: np.ndarray, axis: int = 0) -> np.ndarray:
    mean_gs = np.mean(graph_signal, axis=axis, keepdims=True)
    std_gs = np.std(graph_signal, axis=axis, keepdims=True)
    return (graph_signal - mean_gs) / std_gs
