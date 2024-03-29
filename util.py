import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import os
from pygsp import graphs
from scipy.sparse import find

class GraphD:
    def __init__(self) -> None:
        #networkx object
        self.G = nx.Graph()

class DiGraphD:
    def __init__(self) -> None:
        #networkx object
        self.G = nx.DiGraph()


def draw_graph(G,pos,data=None):
    position = {
            k: tuple(v) for k, v in enumerate(pos)
        }
    W = find(G.W)
    W_list = [[int(W[0][i]),int(W[1][i])] for i in range(len(W[0]))]
    if G.is_directed()==True:
        graphD = DiGraphD()
        graphD.G.add_edges_from([int(W[0][i]),int(W[1][i])] for i in range(len(W[0])))
    else:
        graphD = GraphD()
        graphD.G.add_edges_from(W_list)
    fig, ax = plt.subplots()
    if isinstance(data, np.ndarray):
        mean = sum(data)/len(data)
        node_sizes = [20*float(signal / mean) for signal in data]
        nx.draw_networkx_nodes(graphD.G, position, node_color=data, cmap='turbo', node_size=node_sizes)
        """カラーバーの追加"""
        sm = plt.cm.ScalarMappable(cmap='turbo', norm=plt.Normalize(vmin=min(data), vmax=max(data)))
        sm.set_array([0,max(data)])  # カラーマップの範囲を設定
        cbar = plt.colorbar(sm, ax=ax)  # ax引数を指定
    else:
        nx.draw_networkx_nodes(graphD.G, position, node_size=10)

    nx.draw_networkx_edges(graphD.G, position, width=0.2)
    plt.show()
    plt.close(fig)


if __name__ == '__main__':
    files = [filename for filename in os.listdir('dataset_ver4.0') ]
    for i in range(len(files)):
        npz = np.load(os.path.join('dataset_ver4.0',files[i]))
        N,T,W,L,data,pos = npz['N'],npz['T'],npz['W'],npz['L'],npz['data'],npz['pos']
        G = graphs.Graph(W)
        draw_graph(G,data[:,0],pos)
        npz.close()