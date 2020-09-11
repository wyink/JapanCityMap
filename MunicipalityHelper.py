import re
import json
from collections import OrderedDict
from typing import Dict, List, TypeVar
import City
import CitySet

#type-alias
TDSLi   = Dict[str,List[int]]
TDSI    = Dict[str,int]
TLi     = List[int]
TLs     = List[str]
TDSLs   = Dict[str,List[str]]
C = TypeVar('C') #City


class MunicipalitiesHelper:
    pass

def main():
    #svgファイルの読み込み
    infile1 = "tmp/OsakaMap.svg"
    order_path_sorted = read_svg(infile1)

    #geojsonファイルの読み込み
    infile2 = "./data/N03-200101_27_GML/N03-20_27_200101.geojson"
    code_property_sorted = read_geojson(infile2)

    #cityオブジェクトの生成
    cityset = create_city_object(
                    code_property_sorted,
                    order_path_sorted
                )

    #各エリアを示すpathタグのカウンタとその場所を保持する
    #cityを結びつける．
    #area_citycode = path_cityobject_linker(cityList)

    #白地図の出力
    outfile = "tmp/OsakaMap_brank2.svg"
    output_svg(infile1,outfile,cityset)



        
def color_pathtag_linker(lines):
    '''カラーコードとpathタグのカウンタの対応

        Dict[citycode : List[area]]
        に対応する辞書である
        Dict[colorcode : List[pathタグのカウンタ]]
        を返却する関数

        ・各pathタグのカウンタは一つのエリアに対応
        ・各行政地区は複数のエリアを保持
        
        Params
        ------
        lines : List[str]
            入力ファイルの一行分の文字列リスト
            のうち、エリア描画部分のsvg記述

        Returns
        -------
        Dict[str , List[int]]
            key : カラーコード
            val : pathタグのカウンタのリスト

    '''

    ccpa = {}
    pathNum =0  #svgを読み込む際に登場した順番に振られたカウンタ 
    for l in lines:
        colorcode = re.search(r'<path style="fill-rule.+:rgb\((.+?)\);fill-opacity',l).group(1);
        if colorcode in ccpa:
            ccpa[colorcode].append(pathNum)
        else:
            ccpa[colorcode] = [pathNum]
        pathNum += 1

    return ccpa


def colorindex_pathtag_linker(ccpa,ccoa):
    '''色指標のカウンタと行政地区コードの対応

    Dict[citycode , List[area]]
    に対応する辞書
    Dict[the counter of colorIndex , List[pathタグのカウンタ]]
    を返す関数

    色指標のカウンタ（昇順）は行政地区コード（昇順）と1:1で対応

    Parameters
    ----------
    ccpa : Dict[str , List[int]]
        key : カラーコード
        val : pathタグのカウンタのリスト
        
        ex. dict[#FFFFFF] = [1,3,5]

    
    ccoa : Dict[str , int]
        key : カラーコード
        val : 色指標のカウンタ

        ex. dict[#FFF] = 3

    Returns
    -------
    Dict[str , List[int]]
        key : 入力svgファイルの色指標のカウンタ
        val : pathタグのカウンタのリスト

        ex. dict[order]=[1,3]

    
    '''

    colorindex_pathtag = {} 
    for colorcode,order in ccoa.items():
        colorindex_pathtag[order] = ccpa[colorcode]
    
    return colorindex_pathtag
        


def read_svg(infile):
    '''色指標のカウンタとpathタグのカウンタを対応
    
    色指標のカウンタ（昇順）は行政地区コード（昇順）に1:1で対応
    pathタグはsvgファイルでのエリアに対応している．
    read_geojson関数で実際の行政地区コードとこのエリアを対応付ける
    前処理をこの関数では行う．

    Parameters
    ----------
    infile : str
        入力ファイル名（パス）

    Returns
    -------
    Dict[int , List[int]]
        key : 色指標のカウンタ
        val : pathタグのカウンタのリスト

    '''

    ccpa:TDSLi  ={}   #[ColorCode : List[pathタグのカウンタ]]
    ccoa:TDSI   ={}    #[ColorCode : 色指標のカウンタ]
    lines:TLs   =[]

    flag,order,colorcode = 1,0,''

    #カラーコードとpathタグのカウンタを対応
    for l in open(infile,encoding='utf-8'):
        l = l.rstrip()
        if flag==1 and l.startswith('<path style="fill-rule:evenodd'):
            flag=1
            lines.append(l)
            continue
        elif l.startswith('<g style'):
            flag=0
            ccpa = color_pathtag_linker(lines)
            continue
        else:
            if l.startswith('<path style="fill-rule:even'):
                colorcode = re.search(r'rgb\((.+?)\);fill-opacity:',l).group(1)
                ccoa[colorcode] = order
                order += 1
    
    #色指標のカウンタとpathタグのカウンタを対応
    ci_pathtag = colorindex_pathtag_linker(ccpa,ccoa)
    
    ci_pathtag_sorted = {}
    for order,path in sorted(ci_pathtag.items(),key=lambda x:x[0]) :
        ci_pathtag_sorted[order] = path

    return ci_pathtag_sorted

def read_geojson(infile):
    '''行政地区コードと対応する属性を取得

    行政地区コードはCityクラスで扱う最小単位である．
    これをキーとして県名・支庁名・群名/政令指定都市名
    市区町村名を対応付けする．

    Parameters
    ----------
    infile : str
        入力ファイル（拡張子geojson）
    
    Returns
    -------
    Dict[str , List[str]]
        key : 行政地区コード
        val : 県名,支庁名、群・政令指定都市名・市区町村名

        ex. dict[27107] : List['大阪府','',堺市,港区]]

    '''

    code_property:TDSLs ={} #[citycode : List[prefec,branch,county,city]]

    with open(infile,encoding='UTF-8')as f:
        d = json.load(f,object_pairs_hook=OrderedDict)    

    prefec,branch,county,city,citycode = '','','','',''
    for i in d['features']:
        for property,value in i['properties'].items() :
            if  (property=='N03_001'): #県
                prefec = value
            elif(property=='N03_002'): #支庁
                branch = value
            elif(property=='N03_003'): #群・政令指定都市
                county = value
            elif(property=='N03_004'): #市区町村
                city = value
            elif(property=='N03_007'): #市区町村コード
                citycode = value
            elif(property == '_fillOpacity'):
                code_property[citycode]=[prefec,branch,county,city]
            else:
                continue

    code_property_sorted:TDSLs = {} #[citycode : List[prefec,branch,county,city]]

    for code,prop in sorted(code_property.items(),key=lambda x:x[0]):
        code_property_sorted[code] = prop 
    return code_property_sorted

def create_city_object(code_property_sorted,ci_pathtag_sorted):
    '''行政地区コードととpathタグのカウンタを結びつける

    行政地区コードとcode_property_sortedが保持する各属性値、
    およびpathタグのカウンタを結びつける．
    各行政地区コードおよびこれに紐づけされる各要素をともにメンバ関数
    とするCityオブジェクトを作成する．

    Parameters
    ----------
    code_property_sorted : Dict[str , List[str]]
        key : 行政地区コード
        val : 県名・支庁名・群名または政令指定都市名・市区町村名のリスト
    
    ci_pathtag_sorted : Dict[str , List[int]]
        key : 入力svgファイルの色指標のカウンタ
        val : pathタグのカウンタのリスト

    Returns
    --------
    CitySet
        入力ファイルから作成されたcityオブジェクトの全て
        が格納されたリスト
    

    '''
    pathList:TLi = []
    cityList:List[C] = []
    order=0

    for citycode,property in code_property_sorted.items():
        pathList = ci_pathtag_sorted[order]
        city = City.City(citycode,property,pathList,'#FFFFFF')
        cityList.append(city)
        order += 1
    
    cityset = CitySet.CitySet(cityList)
    return cityset

'''
def path_cityobject_linker(cityList) :
    area_citycode = {} 
    for city in cityList:
        for area in city.areablocks_getter():
            area_citycode[area] = copy.copy(city)
    return area_citycode
'''

def output_svg(infile,outfile,cityset):
    flag,rowNum,retflag=1,0,0
    ccobj,code = '',''

    f = open(outfile,'w',encoding='utf-8')
    for l in open(infile,encoding='utf-8'):
        l = l.rstrip()
        if re.search('use xlink:href',l):
            retflag=1
            f.write(l+'\n')
            continue
        if retflag==1 and l.startswith('<path style='):
            break
        if flag==1 and l.startswith('<path style="fill-rule:evenodd'):
            flag=1
            ccobj = re.search(r'<path (style="fill-rule.+;)fill:rgb\(.+?\);(fill-opacity.+$)',l)
            city = cityset.get_city_from_pathnum(rowNum)
            cityname = city.cityname
            f.write('<path class="cwtv {} {}" {}fill:white;{}\n'.format(code,cityname,ccobj.group(1),ccobj.group(2)))
            rowNum+=1
        elif l.startswith('<g style'):
            f.write(l+'\n')
            flag=0
            continue
        else:
            if l.startswith('<path style="fill-rule:even'):
                continue
            else:
                f.write(l+'\n')

    f.write('</g>\n</svg>\n')
    f.close()

if __name__ == "__main__":
    main()

