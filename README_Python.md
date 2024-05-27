![](doc/logo.png)

# GSP-Traffic Dataset

Authors : 
    Rui Kumagai ([r.kumagai@msp-lab.org](<mailto:r.kumagai@msp-lab.org>)), 
    Hayate Kojima ([h-kojima@msp-lab.org](<mailto:h-kojima@msp-lab.org>)), 
    Hiroshi Higashi ([higashi@comm.eng.osaka-u.ac.jp](<mailto:higashi@comm.eng.osaka-u.ac.jp>)), 
    and Yuichi Tanaka ([ytanaka@comm.eng.osaka-u.ac.jp](<mailto:ytanaka@comm.eng.osaka-u.ac.jp>))

## Abstract

Data analysis on graphs, including graph signal processing and graph neural networks, is an emerging research field in signal processing and machine learning. 
To quantitatively compare the performance of these methods, reliable datasets containing graphs as well as graph signals are required. 

Then, we propose GSP-Traffic Dataset, a large-scale time-varying graph signal dataset on simulated traffic networks. 
Our dataset utilizes a traffic flow simulator ["Simulation of Urban MObility" (SUMO)](https://eclipse.dev/sumo/).
SUMO can simulate traffic flows under consistent conditions across multiple cities, facilitating easy comparison of graph properties and features. 
It can also utilize actual road networks: This makes the dataset reliable.

GSP-Traffic Dataset is created based on virtual measurements of traffic volume across 465 cities around the world. 
In the dataset, a graph represents a road network where intersections are vertices and roads are edges. 
All the networks are taken from [Open Street Map](https://www.openstreetmap.org/#map=6/35.588/134.380), i.e., real road networks. 
Signals in the dataset are the total number of vehicles passing through intersections obtained by extensive SUMO simulations.
The measurement period is set to 500 seconds. 
To obtain time-varying signals, the entire simulation period is set to 50,000 seconds.

## Overview

In this section, we show the characteristics of the graphs and signals of our dataset.
(The list of all cities in the dataset is available in [google spreadsheet](https://docs.google.com/spreadsheets/d/1wJ3MPm5TSh5eKkXRGtqZykiy-HV7anCL_F4yfKACNqo/edit?usp=sharing))

The table below shows the statistics of the number of vertices and edges.
|   | max | min | mean | median | std | meandegree |
|--:|---:|----:|------:|--------:|---:|-----------:|
| #vertex | 1399 | 102 | 350.54 | 306 | 222.03 | -|
| #edge | 1979 | 125 | 479.88 | 426 | 303.87 | 2.74|

The image below shows the mean signal values and standard deviation in each city of the GSP-Traffic Dataset.

![](doc/signal_map.jpeg)

The image below shows the mean and standard deviation of log-energy distribution in the graph frequency domain.

![](doc/log_ene.jpeg)

## Installation

Access is possible to clone the git repository at

```sh
git clone https://github.com/kumagai-r-ou/GSP-Traffic-Dataset
```


## Attribute
For each of the 465 cities, the following data is stored in  `(country)_(city).npz`.

The folder named `dataset` contains all the cities, while the folders named `train` and `test` contain cities selected randomly in a 7:3 ratio.

| variable | attribute | shape |
| -------: | -------: | ----: |
| ` N ` | number of nodes | $` 1 `$ |
| ` T ` | number of time-series | $` 1 `$ |
| ` L ` | Graph Laplacian | $` N \times N `$ |
| ` W ` | Weighted matrix | $` N \times N `$ |
| ` data ` | TV graph signals | $` N \times T `$ |
| ` pos ` | `(longitude,latitude)` of the nodes | $` N \times 2 `$ | 


## Citation
If you use this dataset for your research, you may use this bibtex citation:

```bibtex
@conference{gsp_traffic,
    title = {GSP-Traffic Dataset: Graph signal processing dataset based on traffic simulation},
    author = {Kumagai, Rui and Kojima, Hayate and Higashi, Hiroshi and Tanaka, Yuichi},
    booktitle = {Graph Signal Processing Workshop 2024, Delft, The Netherlands},
    year = {2024},
    month = {Jun},
}
```

## Examples

The examples use [pygsp](https://pygsp.readthedocs.io/en/stable/).
If you would like to know the details of some functions, please also refer to the Github of pygsp.

### Loading Data

You can load data by specifying the city and country as follows:

```py
import util
import numpy as np
from pygsp import graphs

npz_path = util.top_dir() / "train" / "Italy_Rome.npz"
npz = np.load(npz_path)
N, T, W, L, data, pos = (
    npz["N"],
    npz["T"],
    npz["W"],
    npz["L"],
    npz["data"],
    npz["pos"],
)

G = graphs.Graph(W)
```

### Signal Filtering

In the following part, we show a simple denoizing experiment.
Firstly, normalize and put a noize as follows:

```py
### Noise vector
data_size = data.shape[0]
noize_signal = np.random.normal(loc=0, scale=0.75, size=data_size)

### Normalize data
normilized_data = util.normalize_graph_signal(data[:, t])
noizy_signal = normilized_data + noize_signal

### Plot signal
util.draw_graph(
    G,
    pos,
    data[:, t],
    image="Italy_Rome_normalized_signal.png",
    use_node_values=normilized_data,
    fig_title="Normalized Signal",
)
util.draw_graph(
    G,
    pos,
    data[:, t],
    image="Italy_Rome_noisy_signal.png",
    use_node_values=noizy_signal,
    fig_title="Noizy Signal",
)
```

#### Output

<p>
	<img src="doc/py_figs/Italy_Rome_normalized_signal.png" width="40%">
	<img src="doc/py_figs/Italy_Rome_noisy_signal.png" width="40%">
</p>

### Design filter

Then, design a low-pass filter as follows:

```py
## Design filter
g = util.gsp_design_smooth_indicator(G, 0, 0.5)
x = g.filter(noizy_signal)
f = util.apply_gft_to_signal(G, normilized_data)
util.save_gs_spectrum(
    f, save_image_name="Italy_Rome_spectrum.png", fig_title="Signal Spectrum"
)
util.save_filter(g, "Italy_Rome_filter.png", fig_title="Filter")
```

#### Output

<p>
	<img src="doc/py_figs/Italy_Rome_spectrum.png" width="40%">
	<img src="doc/py_figs/Italy_Rome_filter.png" width="40%">
</p>

#### Plot results

The result of the experiment is shown as follows:


```py
default_mse = np.sqrt(np.sum((normilized_data - noizy_signal) ** 2)) / 279
filtered_mse = np.sqrt(np.sum((normilized_data - x) ** 2)) / 279

## Plot results
util.draw_graph(
    G,
    pos,
    data[:, t],
    image="Italy_Rome_noisy_signal_with_mse.png",
    use_node_values=noizy_signal,
    fig_title=f"Noizy Signal - MSE: {default_mse:.4f}",
)
util.draw_graph(
    G,
    pos,
    data[:, t],
    image="Italy_Rome_filtered_signal.png",
    use_node_values=x,
    fig_title=f"Filtered Signal - MSE: {filtered_mse:.4f}",
)
```

<p>
	<img src="doc/py_figs/Italy_Rome_noisy_signal_with_mse.png" width="40%">
	<img src="doc/py_figs/Italy_Rome_filtered_signal.png" width="40%">
</p>



## Utility functions

### plotting graph

```py
util.draw_graph(
    G,
    pos,
    data=None,
    image=None,
    fig_titile=None,
    use_node_values=None,
    node_value_disabled=False,
)
```

Draw the graph `G` with `matplotlib`.

You don't have to give `data` when you draw the graph `G` as a simple representation.
If you want to draw the graph `G` reflecting signal values, you need to give `data` at least.

#### parameters:

* `G` : graph

	A pygsp graph.

* `pos` : numpy array ($`N \times 2`$)

	A numpy array representing position of the nodes.

* `data` : numpy array ($`N \times 1`$), optional

	A numpy array representing signal values at time $`t`$.

* `image` : string, optional

    filename to save the image.

* `fig_titile` : string, optional

    A title of figure

* `use_node_values` : numpy array ($`N \times 1`$), optional

    A numpy array representing signal values at time $`t`$. It is assumed that `use_node_values` has the normalized values of `data`.

* `node_value_disabled` : bool, optional

    Set `True` if you draw the graph `G` as a simple representation, otherwise `False`. When you don't set `data`, `node_value_disabled` automatically becomes `True` within the function.


#### Example

```py
util.draw_graph(G, pos, image="Italy_Rome.png", fig_title="Italy - Rome")
```

#### Output
<img src="doc/py_figs/Italy_Rome.png" width="50%">

#### Example

```py
t = 0  # decide the signal time
util.draw_graph(
    G, pos, data[:, t], image="Italy_Rome_signal.png", fig_title="Italy - Rome"
)
```

#### Output

<img src="doc/py_figs/Italy_Rome_signal.png" width="50%">


### plotting filter


```py
util.save_filter(g, filter_name, fig_title=None)
```

Save the filter `g` you made.


#### parameters:

* `g` : filter

    A filter you made.

* `filter_name`: str

    A figure filename of the filter.

* `fig_title`: str, optional

    A title of figure.


#### Example

```py
util.save_filter(g, "Italy_Rome_filter.png", fig_title="Filter")
```

This output example is shown in the section of `Design Smooth Filter`.


### plotting spectrum of graph signals

```py
util.save_gs_spectrum(
    gft_signal, save_image_name, fig_title=None
)
```

Save the spectrum of graph signals.


#### parameters:

* `gft_signal` : spectrum

    Use the spectrum of graph signals.

* `save_image_name`: str

    A figure filename.

* `fig_title`: str, optional

    A title of figure.


#### Example

```py
util.save_gs_spectrum(
    f, save_image_name="Italy_Rome_spectrum.png", fig_title="Signal Spectrum"
)
```

This output example is shown in the section of `Apply GFT to graph signals`.



### Normalize graph signals

```py
normalize_graph_signal(graph_signal, axis=0)
```

Normalize the raw graph signals.

#### parameters:

* `graph_signal` : numpy array ($`N \times 1`$)

    Graph signals

* `axis` : int, optional

    You can set 0 or 1. The processing is conducted along columns if axis=0.


#### Example

```py
normilized_data = util.normalize_graph_signal(data[:, t])
```


### Design Smooth Filter

```py
gsp_design_smooth_indicator(G, a1, a2)
```

Design smooth filter for the graph `G`.
You can keep frequencies of graph signals between `a1` and `a2` and reduce them in other ranges.

#### parameters:

* `G` : graph

    A pygsp graph.

* `a1` and `a2` : float

    `a1` < `a2`. 


#### Example

```py
g = util.gsp_design_smooth_indicator(G, 0, 0.5)
util.save_filter(g, "Italy_Rome_filter.png", fig_title="Filter")
```

Please use `save_filter` to make the figure of constructed filters.

#### Output

<img src="doc/py_figs/Italy_Rome_filter.png" width="40%">


### Apply GFT to graph signals

```py
apply_gft_to_signal(G, graph_signal)
```

`graph_signal` is transformed by using GFT.

#### parameters:

* `G` : graph

    A pygsp graph.
  
* `graph_signal` : numpy array ($`N \times 1`$)

    Raw graph signals


#### Example

```py
f = util.apply_gft_to_signal(G, normilized_data)
util.save_gs_spectrum(
    f, save_image_name="Italy_Rome_spectrum.png", fig_title="Signal Spectrum"
)
```

Please use `save_gs_spectrum` to make the figure of the spectrum of graph signals.

#### Output

<img src="doc/py_figs/Italy_Rome_spectrum.png" width="40%">




