import GSP_TRAFFIC_Python.src.util as util
import numpy as np
from pygsp import graphs
import os

if __name__=='__main__':


    npz = np.load(os.path.join('dataset','Italy_Rome.npz'))
    N,T,W,L,data,pos = npz['N'],npz['T'],npz['W'],npz['L'],npz['data'],npz['pos']
    G = graphs.Graph(W)
    util.draw_graph(G,pos,data[:,0],image='Italy_Rome_signal.png')
    util.draw_graph(G,pos,image='Italy_Rome.png')

    # files = [filename for filename in os.listdir('dataset') ]
    # for i in range(len(files)):
    #     npz = np.load(os.path.join('dataset',files[i]))
    #     N,T,W,L,data,pos = npz['N'],npz['T'],npz['W'],npz['L'],npz['data'],npz['pos']
    #     G = graphs.Graph(W)
    #     util.draw_graph(G,pos,data[:,0])
    #     # util.draw_graph(G,pos)
    #     npz.close()