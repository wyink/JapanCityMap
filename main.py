from module import *

def main():
    #svgファイルの読み込み
    infile1 = "tmp/OsakaMap.svg"
    order_path_sorted = SvgUtils.svg_parser(infile1)

    #geojsonファイルの読み込み
    infile2 = "./data/N03-200101_27_GML/N03-20_27_200101.geojson"
    code_property_sorted = GeoJsonUtils.geojson_parser(infile2)


    #cityオブジェクトの生成
    cityset = CityHelper.toCitySet(
                    code_property_sorted,
                    order_path_sorted
                )

    #ユーザーのファイルの読み込み
    infile = "temp.csv"
    delimiter = ","
    CityHelper.update_citycolor(infile,delimiter,cityset)

    #地図の出力
    outfile = "tmp/OsakaMap_colored.svg"
    OutFormat.output_svg(infile1,outfile,cityset)


    


if __name__ == "__main__":
    main()

