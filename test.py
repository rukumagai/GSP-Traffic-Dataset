import util
import numpy as np
from pygsp import graphs
import os

if __name__=='__main__':
    files = [filename for filename in os.listdir('dataset_ver4.0') ]
    for i in range(len(files)):
        npz = np.load(os.path.join('dataset_ver4.0',files[i]))
        N,T,W,L,data,pos = npz['N'],npz['T'],npz['W'],npz['L'],npz['data'],npz['pos']
        G = graphs.Graph(W)
        util.draw_graph(G,pos,data[:,0])
        # util.draw_graph(G,pos)
        npz.close()