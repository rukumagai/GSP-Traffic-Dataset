# GSP-Traffic Dataset

作成者：
	[熊谷塁](<mailto:r.kumagai@msp-lab.org>)，
	[小島颯](<mailto:h-kojima@msp-lab.org>)，
	[東浩志](<mailto:higashi@comm.eng.osaka-u.ac.jp>)，
	[田中雄一](<mailto:ytanaka@comm.eng.osaka-u.ac.jp>)

## Overview

Data analysis on graphs, including graph signal processing and graph neural networks, is an emerging research field in signal processing and machine learning. 
To quantitatively compare the performance of these methods, reliable datasets containing graphs as well as graph signals are required. 
In this stwe propose GSP-Traffic Dataset, a large-scale time-varying graph signal dataset on simulated traffic networks. Our dataset utilizes a traffic flow simulator and it contains graph signals across multiple cities, facilitating easy comparison of graph signal properties and features. 



## Download

Access is possible by using a Git client to clone the repository at
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

| how to call | argument | explanation |
| ----------- | -------- | ----------- |
| draw_graph(G. pos, data) | G : graph <br>  pos : $ N \times 2 $ <br> data : TV signals <br> output_name = 'out' | plotting function. <br> Output name is 'undir.png' |

