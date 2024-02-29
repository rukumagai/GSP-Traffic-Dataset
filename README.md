<script type="text/javascript" async src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-MML-AM_CHTML">
</script>
<script type="text/x-mathjax-config">
 MathJax.Hub.Config({
 tex2jax: {
 inlineMath: [['$', '$'] ],
 displayMath: [ ['$$','$$'], ["\\[","\\]"] ]
 }
 });
</script>

# Dataset of time-varying graph signals 

=============

作成者：熊谷塁 (r.kumagai@msp-lab.org)

## Overview
- 交通流シミュレータSUMOを利用して一定時間間隔ごとの交差点通過量を測定したデータセットです．
- データ数は465
- `dataset.npy`
- 



## Download
↓↓↓↓↓↓↓This is the github link↓↓↓↓↓↓↓
https://github.com/kumagai-r-ou/traffic-dataset-using-sumo

## Attribute

| variable | attribute | shape |
| -------: | :-------: | ----: |
| $ N $ | number of nodes | $ 1 $ |
| $ T $ | number of time-series | $ 1 $ |
| $ L $ | Graph Laplacian | $$ N \times N $$ |
| $ W $ | Weighted matrix | $$ N \times N $$ |
| $ data $ | TV graph signals | $$ N \times T $$ |

## Examples

### python(pygsp)

### python(networkx)

### matlab


## Utility functions

from util import paint_graph

### plotting

| how to call | argument | explanation |
| ----------- | -------- | ----------- |
| paint_graph(G. data, pos) | G : graph <br> data : TV signals <br> pos : $ N \times \|E\| $ <br> output_name = 'out' | plotting function. <br> Output name is 'undir.png' |

