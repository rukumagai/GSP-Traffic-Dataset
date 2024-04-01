# GSP-Traffic Dataset

Authors : [Rui Kumagai](<mailto:r.kumagai@msp-lab.org>), [Hayate Kojima](<mailto:h-kojima@msp-lab.org>), [Hiroshi Higashi](<mailto:higashi@comm.eng.osaka-u.ac.jp>), and [Yuichi Tanaka](<mailto:ytanaka@comm.eng.osaka-u.ac.jp>)

## Overview

Data analysis on graphs, including graph signal processing and graph neural networks, is an emerging research field in signal processing and machine learning. 
To quantitatively compare the performance of these methods, reliable datasets containing graphs as well as graph signals are required. 
In this stwe propose GSP-Traffic Dataset, a large-scale time-varying graph signal dataset on simulated traffic networks. Our dataset utilizes a traffic flow simulator and it contains graph signals across multiple cities, facilitating easy comparison of graph signal properties and features. 



## Installation

Access is possible to clone the git repository at
```
git clone https://github.com/kumagai-r-ou/traffic-dataset-using-sumo
```


## Attribute

| variable | attribute | shape |
| -------: | :-------: | ----: |
| $ N $ | number of nodes | $ 1 $ |
| $ T $ | number of time-series | $ 1 $ |
| $ L $ | Graph Laplacian | $$ N \times N $$ |
| $ W $ | Weighted matrix | $$ N \times N $$ |
| $ data $ | TV graph signals | $$ N \times T $$ |
| $ pos $ | (longitude,latitude) of the nodes | $$ N \times 2 $$ | 

## Examples

### python(pygsp)
```
import numpy as np
from pygsp import graphs

npz = np.load(filename)
N,T,W,L,data,pos = npz['N'], npz['T'], npz['W'], npz['L'], npz['data'], npz['pos']
G = graphs.Graph(W)
draw_graph(G,data[:,0],pos)
```

### matlab


## Utility functions

from util import draw_graph
### plotting

Draw the graph G with matplotlib.

You don't have to give `data` when you draw the graph G as a simple representation.
If you want to draw the graph G reflecting signal values, you can give `data` 
```
draw_graph(G, pos, data=None)
```

parameters:

`G`:graph

A pygsp graph

`pos`:numpy array ($`N \times 2`$)

A numpy array representing position of the nodes.

`data`:numpy array ($`N \times 1`$), optional