from CitySet import CitySet
from collections import OrderedDict
from typing import Dict, List,TypeVar
import json
import re

#type-alias
TDSLi   = Dict[str,List[int]]
TDSI    = Dict[str,int]
TLs     = List[str]
TLi     = List[int]
TDSLs   = Dict[str,List[str]]
C = TypeVar('C') #City



class SvgUtils :

    @staticmethod
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
                ccpa = SvgUtils._color_pathtag_linker(lines)
                continue
            else:
                if l.startswith('<path style="fill-rule:even'):
                    colorcode = re.search(r'rgb\((.+?)\);fill-opacity:',l).group(1)
                    ccoa[colorcode] = order
                    order += 1
        
        #色指標のカウンタとpathタグのカウンタを対応
        ci_pathtag = SvgUtils._colorindex_pathtag_linker(ccpa,ccoa)
        
        ci_pathtag_sorted = {}
        for order,path in sorted(ci_pathtag.items(),key=lambda x:x[0]) :
            ci_pathtag_sorted[order] = path
    
        return ci_pathtag_sorted
    

    
    @staticmethod
    def _colorindex_pathtag_linker(ccpa,ccoa):
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

    @staticmethod
    def _color_pathtag_linker(lines):
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
            colorcode = re.search(r'<path style="fill-rule.+:rgb\((.+?)\);fill-opacity',l).group(1)
            if colorcode in ccpa:
                ccpa[colorcode].append(pathNum)
            else:
                ccpa[colorcode] = [pathNum]
            pathNum += 1

        return ccpa


class GeoJsonUtils :

    @staticmethod
    def read_geojson(infile):
        '''行政地区コードと対応する属性を取得

        行政地区コードはCityクラスで扱う最小単位である．
        これをキーとして県名・支庁名・郡名/政令指定都市名
        市区町村名を対応付けする．

        Parameters
        ----------
        infile : str
            入力ファイル（拡張子geojson）

        Returns
        -------
        Dict[str , List[str]]
            key : 行政地区コード
            val : 県名,支庁名、郡・政令指定都市名・市区町村名

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
                elif(property=='N03_003'): #郡・政令指定都市
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

class UserfileUtils :

    
    @staticmethod
    def change_color_from_citycode(infile:str, delimiter:str, cityset:CitySet):
        '''行政地区コードを指定して色を変更する
        '''
        for l in infile:
            l = l.strip()
            citycode,colorcode = l.split(delimiter,1)

            #入力ファイルの第一カラムに対応するcitycodeを検索
            city = cityset.get_city_from_citycode(citycode)

            #第二カラムに指定されたカラーコードに変更   
            city.colorcode(colorcode)
    
        return cityset

    @staticmethod
    def change_color_from_county(infile:str, delimiter:str, cityset:CitySet):
        '''市区町村名・もしくは郡・政令指定都市名を指定して色を変更する

        大阪府の場合，大阪市や堺市、また泉北郡・南河内郡などがあり、これらと
        貝塚，岸和田市などが混在している場合でも利用可能

        例
            Ok!      堺市，能勢町，岸和田市
            Not Ok!  堺市，港区（堺市に属する）
                この場合は後に読み込まれた行政地区に上書きされる．
                （必ずしも期待した出力結果でない可能性がある） 
        
        '''

        for l in infile:
            l = l.strip()
            county,colorcode = l.split(delimiter,1)

            cityList = [] # type : List[City]
            if cityset.isCounty(county) : #入力した値が郡・政令指定都市かどうかの判定
                cityList = cityset.get_city_from_county('All') 
                for city in cityList:           
                   city.colorcode(colorcode)
            else:#市区町村名であると判定
                city = cityset.get_city_from_cityname(county)
                city.colorcode(colorcode)               
            
        return cityset


