![](image/logo.png)

# GSP-Traffic Dataset

Authors : 
    [Rui Kumagai](<mailto:r.kumagai@msp-lab.org>), 
    [Hayate Kojima](<mailto:h-kojima@msp-lab.org>), 
    [Hiroshi Higashi](<mailto:higashi@comm.eng.osaka-u.ac.jp>), 
    and [Yuichi Tanaka](<mailto:ytanaka@comm.eng.osaka-u.ac.jp>)

## Overview

Data analysis on graphs, including graph signal processing and graph neural networks, is an emerging research field in signal processing and machine learning. 
To quantitatively compare the performance of these methods, reliable datasets containing graphs as well as graph signals are required. 

Then, we propose GSP-Traffic Dataset, a large-scale time-varying graph signal dataset on simulated traffic networks. 
Our dataset utilizes a traffic flow simulator ["Simulation of Urban MObility" (SUMO)](https://sumo.dlr.de/docs/index.html).
SUMO can simulate traffic flows under consistent conditions across multiple cities, facilitating easy comparison of graph properties and features. 
It can also utilize actual road networks: This makes the dataset reliable.

GSP-Traffic Dataset is created based on virtual measurements of traffic volume across 465 cities around the world. 
In the dataset, a graph represents a road network where intersections are vertices and roads are edges. 
All the networks are taken from [Open Street Map](https://www.openstreetmap.org/#map=6/35.588/134.380), i.e., real road networks. 
Signals in the dataset are the total number of vehicles passing through intersections obtained by extensive SUMO simulations.
The measurement period is set to 500 seconds. 
To obtain time-varying signals, the entire simulation period is set to 50,000 seconds.

## Installation

Access is possible to clone the git repository at
```
git clone https://github.com/kumagai-r-ou/GSP-Traffic-Dataset
```


## Attribute
For each of the 465 cities, the following data is stored in  `(country)_(city).npz`.

The folder named `dataset` contains all the cities, while the folders named `train` and `test` contain cities selected randomly in a 7:3 ratio.

| variable | attribute | shape |
| -------: | :-------: | ----: |
| ` N ` | number of nodes | $` 1 `$ |
| ` T ` | number of time-series | $` 1 `$ |
| ` L ` | Graph Laplacian | $` N \times N `$ |
| ` W ` | Weighted matrix | $` N \times N `$ |
| ` data ` | TV graph signals | $` N \times T `$ |
| ` pos ` | (longitude,latitude) of the nodes | $` N \times 2 `$ | 

## Examples

### python(with [pygsp](https://pygsp.readthedocs.io/en/stable/))
```
import os
import numpy as np
from pygsp import graphs

files = [filename for filename in os.listdir('dataset') ]

npz = np.load(os.path.join('dataset',files[0]))
N,T,W,L,data,pos = npz['N'], npz['T'], npz['W'], npz['L'], npz['data'], npz['pos']
G = graphs.Graph(W)

t = 0    
draw_graph(G,data[:,t],pos)
```

### matlab

coding in progress...

## Utility functions
### plotting
```
draw_graph(G, pos, data=None, image=None)
```
Draw the graph G with matplotlib.

You don't have to give `data` when you draw the graph G as a simple representation.
If you want to draw the graph G reflecting signal values, you can give `data`.

#### parameters:

* `G` : graph

	A pygsp graph.

* `pos` : numpy array ($`N \times 2`$)

	A numpy array representing position of the nodes.

* `data` : numpy array ($`N \times 1`$), optional

	A numpy array representing signal values at time $`t`$.

* `image` : string, optional

    filename to save the image. 


#### Example
```
from util import draw_graph()

npz = np.load(os.path.join('dataset','Italy_Rome.npz'))
N,T,W,L,data,pos = npz['N'],npz['T'],npz['W'],npz['L'],npz['data'],npz['pos']
G = graphs.Graph(W)

util.draw_graph(G,pos,image='Italy_Rome.png')
```
#### Output
![](image/Italy_Rome.png)

#### Example
```
from util import draw_graph()

npz = np.load(os.path.join('dataset','Italy_Rome.npz'))
N,T,W,L,data,pos = npz['N'],npz['T'],npz['W'],npz['L'],npz['data'],npz['pos']
G = graphs.Graph(W)

util.draw_graph(G,pos,data[:,0],image='Italy_Rome_signal.png')
```

#### Output
![](image/Italy_Rome_signal.png)