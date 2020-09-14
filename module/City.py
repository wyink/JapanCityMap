from typing import List


class City:
    '''行政地区の情報を管理するクラス
    
    Attributes
    ----------
    citycode:int
        行政地区コード 
    prefec:str
        都道府県名
    branch:str
        支庁名
    county:str
        郡および政令指定都市名
    cityname:str
        市区町村名  
    areablocks:List[int]
        svgに出現したpathタグのカウンタリスト
        各行政地区に属するエリアを保持する．   
    order:int
        svgに出現した色指標の順番
        昇順に並べたとき，行政地区コードの昇順に対応．   
    colorcode:str
        エリアを塗りつぶすカラーコード
    '''

    def __init__(self, citycode:str, property:List[str], areablocks:List[int], order:int, colorcode='#FFFFFF'):
        self._citycode = citycode
        self._prefec = property[0]
        self._branch = property[1]
        self._county = property[2]
        self._cityname = property[3]
        self._areablocks = areablocks
        self._order = order
        self._colorcode = colorcode     #colorcodeのみ変更可能
    
    @property
    def citycode(self)->str:
        return self._citycode

    @property
    def prefec(self)->str:
        return self._prefec
    
    @property
    def branch(self)->str:
        return self._branch
    
    @property
    def county(self)->str:
        return self._county

    @property
    def cityname(self)->str:
        return self._cityname

    def areablocks(self)->List[int]:
        return self._areablocks
    
    @property
    def order(self)->int:
        return self._order
    
    @property
    def colorcode(self)->str:
        return self._colorcode
    
    @colorcode.setter
    def colorcode(self, colorcode:str):
        self._colorcode = colorcode

    
    def isCounty(self)->bool:
        '''cityが郡・政令指定都市に所属するかの判定

        Returns
        -------
        bool 
            True : cityが郡もしくは政令指定都市に所属する．
            False : 郡もしくは政令指定都市に所属しない．
        
        '''
        
        return True if self._county else False
        
