from typing import Dict, List,TypeVar
import CitySet
import City

#type-alias
TDSLi   = Dict[str,List[int]]
TDSI    = Dict[str,int]
TLs     = List[str]
TLi     = List[int]
TDSLs   = Dict[str,List[str]]
C = TypeVar('C') #City

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
