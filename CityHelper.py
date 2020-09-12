from typing import Dict, List,Tuple
from CitySet import CitySet
from City import City


class CityHelper:
    '''svg,geojsonを利用したCitySetオブジェクト作成の支援
    
    SvgUtils,GeojsonUtils関数で作成した辞書を利用してCitySet
    （Cityのセット）を作成して返却する

    '''

    @staticmethod
    def toCitySet(code_property_sorted,ci_pathtag_sorted):
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
        pathList= []  # type: List[int]
        cityList= []  # type: List[City]
        order=0

        for citycode,property in code_property_sorted.items():
            pathList = ci_pathtag_sorted[order]
            city = City(citycode,property,pathList,order,'#FFFFFF')
            cityList.append(city)
            order += 1

        cityset = CitySet(cityList)
        return cityset


    @staticmethod
    def update_citycolor(infile:str, delimiter:str, cityset:CitySet):
        '''入力ファイルからcitysetに含まれるcityの色を変更
        '''

        city_color,ctype = CityHelper.load_infile(infile, delimiter) 

        if ctype:
            CityHelper._update_color_from_citycode(city_color,cityset)
        else:
            CityHelper._update_color_from_county(city_color,cityset)


    @staticmethod
    def load_infile(infile:str, delimiter:str)-> Tuple[Dict[str ,str],bool]:

        city_color = {} #type : Dict[str,str]
        city,color = '',''
        for l in open(infile,"r",encoding="UTF-8") :
            l = l.strip()
            city,color = l.split(delimiter,1)
            city_color[city] = color

        rettype = CityHelper._is_citycode(city)

        return city_color,rettype
    
    @staticmethod
    def _is_citycode(city:str):
        '''入力ファイルの第一カラムが行政地区コードであるか否か
        第一カラムの候補としては行政地区コードの他に市区町村名
        （郡・政令指定都市名の混在）がある．この判定をここで行う．
        '''
        return True if city.isdecimal() else False

        
    @staticmethod
    def _update_color_from_citycode(city_color:Dict[str, str], cityset:CitySet):
        '''行政地区コードを指定して色を変更する
        '''
        for citycode,color in city_color.items():
            #入力ファイルの第一カラムに対応するcitycodeを検索
            city = cityset.get_city_from_citycode(citycode)
            #第二カラムに指定されたカラーコードに変更   
            city.colorcode = color
        return cityset

    @staticmethod
    def _update_color_from_county(city_color:Dict[str, str], cityset:CitySet):
        '''市区町村名・もしくは郡・政令指定都市名を指定して色を変更する
        大阪府の場合，大阪市や堺市、また泉北郡・南河内郡などがあり、これらと
        貝塚，岸和田市などが混在している場合でも利用可能
        例:
            Ok!      堺市，能勢町，岸和田市
            Not Ok!  堺市，港区（堺市に属する）
                この場合は後に読み込まれた行政地区に上書きされる．
                （必ずしも期待した出力結果でない可能性がある） 
        '''
        for county,color in city_color.items():
            cityList = [] # type : List[City]
            if cityset.isCounty(county) : #入力した値が郡・政令指定都市かどうかの判定
                cityList = cityset.get_city_from_county(county) 
                for city in cityList:         
                   city.colorcode = color
            else:#市区町村名であると判定
                city = cityset.get_city_from_cityname(county)
                city.colorcode = color              
        return cityset

        

