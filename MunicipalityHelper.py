import sys
import re
import json
import copy
from collections import OrderedDict


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
    cityList = create_city_object(
                    code_property_sorted,
                    order_path_sorted
                )

    #各エリアを示すpathタグの出現順序とその場所を保持する
    #cityを結びつける．
    area_citycode = path_cityobject_linker(cityList)

    #白地図の出力
    outfile = "tmp/OsakaMap_brank.svg"
    output_svg(infile1,outfile,cityList,area_citycode)



        
def color_area_linker(lines:list)->dict:
    '''
        Description
        ------------------------------
        dict[行政地区]=[area1,area2...]
        に対応する辞書
        dict[カラーコード] = [<path1>,<path2>...]
        を返す関数

        各pathタグは一つのエリアに対応する．
        各行政地区は複数のエリアを保持する．
        →各行政地区は複数のpathタグを持つ．
        カラーコードと各行政地区は1対1で対応している．
        →各カラーコードは複数のpathタグを持つ．
        
        Params
        ------
        lines:list
            入力ファイルの一行分の文字列リスト
            のうち、エリア描画部分のsvg記述

        Returns
        -------
        ccpa : dict (key:str,value:int)
            ccpa[ColorCode]=[pathNum,pathNum...]

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


def order_pathNum_linker(ccpa:dict,ccoa:dict)->dict:
    '''
    Description
    -----------
    dict[行政地区]=[area1,area2]
    に対応する辞書
    dict[色指標の出現順序]=[<path1>,<path2>...]
    を返す関数

    入力のsvgファイルの色指標の出現順序は行政地区コードを
    昇順に並べた順序と対応している．
    入力のsvgファイルにおける各エリアブロックはpathタグ
    の出現順序（以下pathNum)に対応している．

    Parameters
    ----------
    ccpa : dict(str:list)
        dict[ColorCode] = [pathNum,pathNum,...]
        キーはカラーコード
        値はキーの出現順序に対応するカラーコードを保持する
        pathタグの出現順序のリスト
    
    ccoa : dict(str:int)
        dict[ColorCode] = Order-of-appearance
        キーはカラーコード
        値は色指標の出現順序

    Returns
    -------
    order_path:dict(str:str)
        dict[order]=[pathNUm,pathNum...]
        キーは入力svgファイルの色指標の出現順序
        値はキーの出現順序に対応するカラーコードを保持する
        pathタグの出現順序のリスト
    
    '''

    order_path = {} 
    for colorcode,order in ccoa.items():
        order_path[order] = ccpa[colorcode]
    
    return order_path
        


def read_svg(infile:str)->dict:
    ccpa={} #ccpa[ColorCode] = [pathNum,pathNum,...]
    ccoa={} #ccoa[ColorCode] = Order-of-appearance
    pathNum,flag,order,colorcode = 0,1,0,''
    lines:list=[]


    for l in open(infile,encoding='utf-8'):
        l = l.rstrip()
        if flag==1 and l.startswith('<path style="fill-rule:evenodd'):
            flag=1
            lines.append(l)
            continue
        elif l.startswith('<g style'):
            flag=0
            ccpa = color_area_linker(lines)
            continue
        else:
            if l.startswith('<path style="fill-rule:even'):
                colorcode = re.search(r'rgb\((.+?)\);fill-opacity:',l).group(1)
                ccoa[colorcode] = order
                order += 1
    
    order_path = order_pathNum_linker(ccpa,ccoa)
    
    order_path_sorted = {}
    for order,path in sorted(order_path.items(),key=lambda x:x[0]) :
        order_path_sorted[order] = path

    return order_path_sorted

def read_geojson(infile:str)->dict:
    #code_property[citycode]=[prefec,branch,county,city]
    code_property={} 

    with open(infile,encoding='UTF-8')as f:
        d = json.load(f,object_pairs_hook=OrderedDict)    

    for i in d['features']:
        for property,value in i['properties'].items() :
            if  (property=='N03_001'): #prefecture
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

    code_property_sorted = {}

    for code,prop in sorted(code_property.items(),key=lambda x:x[0]):
        code_property_sorted[code] = prop 
    return code_property_sorted

def create_city_object(code_property_sorted:dict,order_path_sorted:dict)->list:

    order=0
    pathList,cityList = [],[]
    for citycode,property in code_property_sorted.items():
        pathList = order_path_sorted[order]
        city = City(citycode,property,pathList,'#FFFFFF')
        cityList.append(city)
        order += 1
    
    return cityList

def path_cityobject_linker(cityList:list)->dict:
    area_citycode = {} 
    for city in cityList:
        for area in city.areablocks_getter():
            area_citycode[area] = copy.copy(city)
    return area_citycode

def output_svg(infile,outfile,cityList,area_citycode):
    flag,rowNum,retflag=1,0,0
    ccobj,code,jp = '','',''

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
            city = area_citycode[rowNum]
            code = city.citycode_getter()
            cityname = city.cityname_getter()
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

