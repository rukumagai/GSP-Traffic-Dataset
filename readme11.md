SUMOを用いたデータセット作成
=============

SUMOを用いたデータセット作成の流れを解説します。

# 手順
---
基本的にカレントディレクトリはsumoで統一している。
- `python tools/osmWebWizard.py`を実行してOSMを起動。欲しい領域などを設定する

- `sumo -c data_hoge/osm.sumocfg --additional-files 00mycode/add.xml`を実行して`edge_file`についてのデータを収集する。このデータは各交差点における*車両通過量*を記録している。

- `netconvert --sumo-net-file=data_hoge/osm.net.xml -p=data_hoge/region`を実行して`edg.xml`や`nod.xml`を取得する。nodには*各交差点のidや座標*が、edgには*各道路のidや車両流出量*などが記録されている。

- `python 00mycode/edgelist_make.py`を実行する。この関数により道路の接続関係を表す`edgelist.csv`ファイルと、交差点の座標、各timestepにおける車両通過量の統計データが格納された`nodelist.csv`ファイルが生成される。

- `python 00mycode/graph_output.py`を実行して交差点を頂点とした接続方向に有向のグラフ画像を生成する。

# 捕捉

- `sumo -c data_hoge/osm.sumocfg --queue-output data_hoge/queue.xml`を実行すれば信号における待機車両台数のデータが出力される。

- `python tools/xml/xml2csv.py data_hoge/queue.xml`を実行すればxmlファイルをcsvファイルに変換することができる。

- `python　tools/visualization/plot_net_trafficLights.py -n data_hoge/osm.net.xml --xlim 0,12000 --ylim 0,10000 --edge-width .5 --xticks 16 --yticks 16 
--xlabel m --ylabel m --xlabelsize 16 --ylabelsize 16 --width 5 --edge-color #606060 -o data_hoge/traffic_image.png`を実行すれば信号のある交差点をプロットできる。

- `RandomTrips.py`というファイルで交通需要は定義されている．-eという引数でオプションを設定し変更できるが，今回全てのファイルに対して同様に終了時間を変更したいので，もうデフォルトを変更する

##自分用備忘録
いくつかの都市に対して一気に取得する方法
- `python tools/auto_data.py`を実行してscript_sub.jsファイルの先頭に用意した配列内の都市全てに対してosmの地図データを取得する。
- `python 00mycode/`

- `netconvert --sumo-net-file 00data/Japan_Osaka/osm.net.xml.gz -o 00data/Japan_Osaka/osm.net.xml.gz --numerical-ids.node-start 0`を実行すればノードの番号が変わる

aaaa