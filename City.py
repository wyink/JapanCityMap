class City:
    '''
    Description
    -----------
    Cityクラス
    行政地区の情報を管理するクラス
    
    Member
    --------
    citycode:int
        行政地区コード
    
    prefec:str
        都道府県名

    branch:str
        支庁名

    county:str
        群および政令指定都市名

    cityname:str
        市区町村名
    
    areablocks:list[int]
        svgに出現したpathタグのカウンタリスト
        各行政地区に属するエリアを保持する．
    
    colorcode:str
        エリアを塗りつぶす色
        HTMLで表示される形式で保持する．

    '''

    def __init__(self,citycode,property,areablocks,order,colorcode='#FFFFFF'):
        self.citycode = citycode
        self.prefec = property[0]
        self.branch = property[1]
        self.county = property[2]
        self.cityname = property[3]
        self.areablocks = areablocks
        self.order = order
        self.colorcode = colorcode
    

    def citycode_getter(self):
        return self.citycode

    def prefec_getter(self):
        return self.prefec
    
    def branch_getter(self):
        return self.branch
    
    def county_getter(self):
        return self.county

    def cityname_getter(self):
        return self.cityname

    def areablocks_getter(self):
        return self.areablocks
    
    def order_getter(self):
        return self.order
    
    def colorcode_getter(self):
        return self.colorcode
  
