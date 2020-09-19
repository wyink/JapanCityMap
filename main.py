from module import *
import argparse
import glob
import os
import R


def main():

    parser = argparse.ArgumentParser()
    
    #入力csvファイル名指定
    parser.add_argument(
        "csv",
        help="path to infile.csv",
    )

    #文字コード指定
    parser.add_argument(
        "-encoding",
        help="character code in your csv file." ,
        default="CP932"
    )

    #shape/geojsonファイルディレクトリまでのパスを指定
    parser.add_argument(
        "todir",
        help="path to N03-xxxxxx_xx_GML/*shp,geojson",
    )

    #出力svgファイル名指定
    parser.add_argument(
        "out",
        help="filename for output.svg",
    )

    #出力svgファイルの幅指定
    parser.add_argument(
        "-width",
        default=25, 
        type=int ,
        help="svg-width"
    )

    #出力svgファイルの高さ指定
    parser.add_argument(
        "-height",
        default=12, 
        type = int,
        help="svg-height"
    )

    args = parser.parse_args()

    #Rを利用して基本のカラーマップを作成
    R.make_basic_colormap(args.todir, args.width, args.height, args.encoding)

    #行政地区コードとsvgで表現されたエリアの対応付け
    basicsvg = "tmp/tmp.svg"
    order_path_sorted = SvgUtils.svg_parser(basicsvg)

    #行政地区コードと各属性（行政地区名，色他）との対応付け
    geojson = (glob.glob(os.path.join(args.todir,"*.geojson")))[0]
    code_property_sorted = GeoJsonUtils.geojson_parser(geojson)


    #行政地区，svgで表現された各エリアおよび各属性の対応付け
    cityset = CityHelper.toCitySet(
                    code_property_sorted,
                    order_path_sorted
                )

    #任意の色に各行政地区の色を変更
    infile2 = args.csv
    delimiter = ","
    CityHelper.update_citycolor(
            infile2,
            delimiter,
            cityset,
            encoding=args.encoding
        )

    #基本のカラーマップを上書きして出力
    outfile = args.out
    OutFormat.output_svg(basicsvg,outfile,cityset)


if __name__ == "__main__":
    main()

