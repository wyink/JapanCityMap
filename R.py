import pyper
import glob
import os

def make_basic_colormap(todir:str, width:int, height:int, encoding="CP932")->None:
    '''shapeファイルから行政地区単位でカラーマップを作成

    行政地区単位で異なる色で配色される．
    しかしあくまで色と行政地区が対応しているのみで
    行政地区とその名前・コードとの対応はなされない．

    Parameters
    ----------
    todir : str
        shapeファイルまでのディレクトリ
    width : int
        出力svgファイルの幅
    height : int
        出力svgファイルの高さ
    encoding : str
        入力svgファイルに使用されている文字コード

    '''

    #create R object
    r = pyper.R()

    r("library(sf)")
    r("library(ggplot2)")

    #input shapefile
    shapefile = (glob.glob(os.path.join(todir,"*.shp")))[0]
    r.assign('shapefile',shapefile)

    #make tmporary directory.
    os.makedirs('./tmp',exist_ok=True)

    #set output svg file name
    svgfile = './tmp/tmp.svg'
    r.assign('svgfile',svgfile)



    #output OsakaMap
    #Each area are colored according to municipality code.
    r.assign('param1',width)
    r.assign('param2',height)

    encoding_to_r = "ENCODING=" + encoding + '"' 
    r.assign('option',encoding_to_r)

    r('shp <- sf::st_read(shapefile,options=option)')
    r('svg(svgfile, width=param1, height=param2)')
    r('ggplot()+geom_sf(data=shp,aes(fill=N03_007))')
    r('dev.off()')
