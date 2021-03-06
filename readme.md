# JapanCityMap
This program fills each municipality you choose in a prefecture, Japan with a color you like. You can save it in SVG format.

---
## このアプリケーションについて
日本の47都道府県それぞれに割り振られている市区町村を最小単位として自由に色を塗ることができます．対応しているフォーマットはSVGです．

## 使用例
大阪府の色分け </br>
<img src="https://user-images.githubusercontent.com/69898489/93661288-97129200-fa91-11ea-915d-84f48bb9859e.png" width="300">

## 使用方法
使用ソフトウェア
- R-3.x.x 

使用言語
- Python 3.x
</br>

**以下の外部パッケージをインストールする必要があります．**</br>
- **pyperモジュール (python)**</br>
    （Rをpython側から実行するのに必要）</br>
- **sf,ggplot2ライブラリ (R)**</br>
    （描画するのに必要）</br>

**以下の手順でインストールします．** </br>
1. pyperモジュールのインストール</br>
`$ pip install pyper` </br>

2. Rソフトを開き、以下のコマンドを使用して2つの必要パッケージをインストールします．</br>
`> install.packages("sf")` </br>
`> install.packages("ggplot2")`</br>
</br>

3. 対象の県のシェープファイルを以下のサイトから取得する．</br>
[国土交通省のダウンロードページ](https://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-N03-v2_4.html)

4. シェープファイルはzip形式で提供されるため、これを解凍する．

5. 各パラメータを引数としてmain.pyを実行</br>
 `$ python main.py csv todir out [-width WIDTH] [-height HEIGHT] [-encoding ENCODING] ` </br>

   - **`No Such File` というエラーが出た場合はRソフトの実行パスが通っていない可能性があります。**</br>
  
   - 第一引数：csv</br>
   ：入力csvファイル名を指定
   - 第二引数：todir</br>
   ：shape/geojsonファイルディレクトリまでのパスを指定
   - 第三引数：out</br>
   ：出力svgファイル名を指定
   - [ WIDTH ]（正の整数で指定）</br>
   ：出力svgファイルの幅を指定
   - [ HEIGHT ]（正の整数で指定）</br>
   ：出力svgファイルの高さを指定
   - [ ENCODING ] (デフォルトはcp932）</br>
  
  


## 実行例

 ディレクトリ構成例（出力前）
```
 /
 ├─test.csv // 入力csvファイル
 ├─main.py
 ├─R.py
 ├─readme.md
 ├─data
 │  └─N03-200101_27_GML //ダウンロードしたファイル
 └─module
```

 入力ファイル例（test.csv）
 （指定する色は `色名` ， `#rrggbb` に対応）
```
 堺市,Red
 千早赤阪村,#FFFF00
```

パラメータ設定例
```
/* 
 * test.csvを入力ファイルとする
 * 4の解凍後のディレクトリを上のように配置
 * out.svgという名前を付けて保存（カレントディレクトリに生成）
 * 幅を20、高さ20で出力．
 * （幅と高さは任意のオプション/デフォルトはwidth:25,height:12）
 * test.csvはutf-8なのでエンコーディングをutf-8に変更
 * （デフォルトはcp932）
 */
```
 利用コマンド例
```
 $ python main.py test.csv ./data/N03-200101_27_GML out.svg -width 20 -height 20 -encoding UTF-8
```
## 出力例

<img src="https://user-images.githubusercontent.com/69898489/93661156-8dd4f580-fa90-11ea-9531-931785328167.png" width="300">




