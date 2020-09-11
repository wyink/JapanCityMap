from InFileParser import SvgUtils,GeoJsonUtils
from CityHelper import CityHelper
from OutFormat import OutFormat
from CitySet import CitySet


def main():
    #svgファイルの読み込み
    infile1 = "tmp/OsakaMap.svg"
    order_path_sorted = SvgUtils.read_svg(infile1)

    #geojsonファイルの読み込み
    infile2 = "./data/N03-200101_27_GML/N03-20_27_200101.geojson"
    code_property_sorted = GeoJsonUtils.read_geojson(infile2)


    #cityオブジェクトの生成
    cityset = CityHelper.toCitySet(
                    code_property_sorted,
                    order_path_sorted
                )

    '''
    city/colorのファイルを入力とする．
    city include [citycode,cityname,cityname+county]
    
    '''
    #ユーザーのファイルの読み込み(cityname)
    infile = input()
    delimiter = input()
    
    #白地図の出力
    outfile = "tmp/OsakaMap_brank.svg"
    OutFormat.output_svg(infile1,outfile,cityset)


    


if __name__ == "__main__":
    main()

