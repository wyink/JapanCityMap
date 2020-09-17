# JapanCityMap
This program fills each municipality you choose in a prefecture,Japan with a color you like. You can save it in svg format.

---
###このアプリケーションについて
日本の47都道府県それぞれに割り振られている市区町村を最小単位として自由に色を塗ることができます．対応しているフォーマットはsvgです．

###使用例
大阪府の色分け
写真を貼り付け

### 使用方法
使用ソフトウェア
- R-3.x.x 

使用言語
- Python 3.x

以下の外部パッケージをインストールする必要があります．
1. pyperモジュールのインストール（Rをpython側から実行するのに必要）
`$ pip install pyper` 
`C:\Users\***> pip install pyper` (Windows)</br>
</br>
2. Rソフトを開き、以下のコマンドを使用して2つの必要パッケージをインストールします．
`> install.packages("sf")` 
`> install.packages("ggplot2")`
</br>

3. 対象の県のを取得する．



