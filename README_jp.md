# GSP-Traffic Dataset

作成者：
	[熊谷塁](<mailto:r.kumagai@msp-lab.org>)，
	[小島颯](<mailto:h-kojima@msp-lab.org>)，
	[東浩志](<mailto:higashi@comm.eng.osaka-u.ac.jp>)，
	[田中雄一](<mailto:ytanaka@comm.eng.osaka-u.ac.jp>)

## Overview

GSP-Traffic Datasetは，交通ネットワーク上でのシミュレーションにより作成された時変グラフ信号データセットです．
シミュレーションには，交通流シミュレータ ["Simulation of Urban MObility" (SUMO)](https://sumo.dlr.de/docs/index.html) を使用しました．
グラフは，交差点を頂点，道路を辺としており，人口100万人を超える465都市の交通ネットワークを[Open Street Map](https://www.openstreetmap.org/#map=6/35.588/134.380)から取得し，作成されました．
信号値は500秒間に交差点を通過した車両の合計台数です．
時系列データを作成するために，シミュレーションは50000秒間行いました．

このデータセットを用いることにより，グラフ信号および時変グラフ信号を扱うグラフ上データ解析手法の統一的な評価が可能となります．

![](image/italy_rome.png)


## Installation
以下のコマンドを実行し，gitをcloneすることでデータセットにアクセスできます．
```
git clone https://github.com/kumagai-r-ou/GSP-Traffic-Dataset
```

## Attribute

465都市それぞれに対して ``` country_city.npz ``` の形で，以下のデータが格納されています．

| Variable | Attributes | Shape |
| -------: | :-------: | ----: |
| ` N ` | 頂点数 | $` 1 `$ |
| ` T ` | 信号の時間 | $` 1 `$ |
| ` L ` | グラフラプラシアン | $` N \times N `$ |
| ` W ` | 重み付き隣接行列（重みは全て1） | $` N \times N `$ |
| ` data ` | 時変グラフ信号 | $` N \times T `$ |
| ` pos ` | 頂点の座標 (軽度，緯度) | $` N \times 2 `$ | 

## Examples

### python(with [pygsp](https://pygsp.readthedocs.io/en/stable/))
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

いくつかの関数が用意されています．
```
from util import draw_graph
```

### plotting

| How to call | Argument | Explanation |
| ----------- | -------- | ----------- |
| draw_graph(G, pos, data) | G : graph <br> pos : $ N \times 2 $ <br> data : TV signals <br> output_name = 'out' | plotting function. <br> Output name is 'undir.png' |

