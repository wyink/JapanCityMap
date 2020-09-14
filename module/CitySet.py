from .City import City
from typing import Dict, List

class CitySet:
    '''複数のCityオブジェクトを管理するクラス

    Attribute
    ---------
    pathnum_city : Dcit[int , City]
        key : pathタグのカウンタ
        val : keyに該当するpathタグを保持するcityオブジェクト
    citycode_city : Dict[str , City]  
        key : 行政地区コード
        val : keyに該当するcityオブジェクト
    prefec_city : Dict[str , List[City]]
        key : 県名
        val : keyの県名に所属するcityオブジェクトのリスト
    branch_city : Dict[str , City]
        key : 支庁名
        val : keyの支庁に該当するcityオブジェクト
    county_city : Dict[str , City]
        key : 郡・政令指定都市名
        val : keyに所属するcityオブジェクト
    cityname_city : Dict[str , City]
        key : 市町村名
        val : keyに該当するcityオブジェクト
    order_city : Dict[int , City] 
        key : 色指標のカウンタ
        val : keyに該当するcityオブジェクト
    colorcode_city : Dict[str , City] 
        key : カラーコード
        val : keyのカラーコードに該当するcityオブジェクト
    
    '''
    def __init__(self,cityList):
        '''メンバ変数の初期化
        
        Parameters
        ----------
        CityList : List[City]
        
        '''

        self.pathnum_city   = {} # type: Dict[int , City]
        self.citycode_city  = {} # type: Dict[str , City] 
        self.prefec_city    = {} # type: Dict[str , List[City]]
        self.branch_city    = {} # type: Dict[str , City]
        self.county_city    = {} # type: Dict[str , List[City]]
        self.cityname_city  = {} # type: Dict[str , City]
        self.order_city     = {} # type: Dict[int , City] 
        self.colorcode_city = {} # type: Dict[str , City] 

        self.unique_attr_getter(cityList)
    

    def unique_attr_getter(self, cityList:List[City])->None:
        '''Cityの各属性値とそれに対応するインスタンスを連携

        Cityの各属性値には複数の値が存在する．場合によって
        該当属性値を保持するcityインスタンス（コンストラクタ
        で代入されるCityListに含まれるうち）が必要になる．
        そのような場合に備えそれぞれの各属性ごとに辞書を作成
        する．

        一つの属性値に対して複数のcityインスタンスが存在する
        場合はリストで保存する．

        Parameters
        ----------
        cityList : List[City]
            cityオブジェクトを保持するリスト
        
        '''

        for city in cityList:
            
            pathnum = 0
            for pathnum in city.areablocks():
                self.pathnum_city[pathnum] = city

            self.citycode_city[city.citycode]       = city
            self.cityname_city[city.cityname]       = city         
            self.order_city[city.order]             = city    
            self.colorcode_city[city.colorcode]     = city

            if not city.prefec in self.prefec_city :
                self.prefec_city[city.prefec] = [city]
            else:
                self.prefec_city[city.prefec].append(city)

            #支庁が存在しない場合
            if city.branch !='' :
                self.branch_city[city.branch] = city
            
            #郡または政令指定都市が存在しない場合
            if city.county !='' :
                if not city.county in self.county_city:
                    self.county_city[city.county] = [city]
                else:
                    self.county_city[city.county].append(city)

    
    def get_city_from_pathnum(self, pathNum:int)->City:
        '''入力のpathNumに対応するcityインスタンスを返却

        Parameters
        ----------
        pathNum : int
            入力のsvgの<path>の出現順序
            特定のエリアと対応している．

        Returns
        -------
        City
            pathNum番目のsvgタグに対応するエリアのcityオブジェクト．

        '''

        if (pathNum<len(self.pathnum_city)):
            return self.pathnum_city[pathNum]
        else:
            raise ValueError("PathNum value is invalid.")

    
    def get_pathnum_all(self)->List[int]:
        '''cityオブジェクトが持つすべてのpathnum

        このオブジェクトで管理されているcityオブジェクト
        が保持するpathnumを返却する．

        Returns
        -------
        List[int]
            cityオブジェクトが保持するpathnumのリスト

        '''
        return list(self.pathnum_city.keys())

    def get_city_from_citycode(self,citycode)->City:
        '''行政地区コードから対応するcityオブジェクトを取得

        Parameters
        ----------
        citycode : str
            取得したいcityの行政地区コード
        
        Returns
        -------
        City
            citycodeに対応するCityオブジェクト

        '''

        if citycode in self.citycode_city:
            return self.citycode_city[citycode]
        else:
            raise ValueError("CityCode value is invalid.")


    def get_citycode_all(self)->List[str]:
        '''cityオブジェクトが持つすべてのcitycodeを取得

        このオブジェクトで管理されているcityオブジェクト
        が保持するcitycodeを返却する．

        Returns
        -------
        List[str]
            cityオブジェクトが保持するcitycodeのリスト

        '''

        return list(self.citycode_city.keys())

    def get_city_from_cityname(self, cityname:str)->City:
        '''行政地区名から対応するcityオブジェクトを取得

        Parameters
        -----------
        cityname : str
            取得したいcityオブジェクトの行政地区名
        
        Returns
        -------
        City
            citynameに対応するcityオブジェクト

        '''

        if cityname in self.cityname_city:
            return self.cityname_city[cityname]
        else:
            raise ValueError("Cityname value is invalid. ")
    
    def get_city_from_prefec(self,prefec)->List[City]:
        '''県名にから対応するcityオブジェクトのリストを取得

        Parameters
        ----------
        prefec : str
            取得したいcityオブジェクトの県名

        Returns
        -------
        List[City]
            prefecに対応するCityオブジェクトのリスト

        '''

        if prefec in self.prefec_city:
            return self.prefec_city[prefec]
        else:
            raise ValueError("Prefec value is invalid.")
            
    def get_city_from_branch(self,branch)->City:
        '''支庁から対応するcityオブジェクトを取得

        Parameters
        -----------
        branch : str
            取得したいcityオブジェクトの支庁名
        Returns
        -------
        List[City]
            branchに対応するcityオブジェクトのリスト

        '''

        if branch in self.branch_city:
            return self.branch_city[branch]
        else:
            raise ValueError("Branch value is invalid.")
    
    def get_city_from_county(self,county='All')->List[City]:
        '''countyを保持するcityを返却する

        引数にcountyを指定した場合は該当するcounty
        を保持するcityを返却する．
        引数なしで呼び出された場合はcountyを保持する
        すべてのcityを返却する．（cityオブジェクトは
        必ずしもcountyを保持しないため利用されえる．）

        Parameters
        ----------
        county : str
            郡・および政令都市名

        Returns
        -------
        List[City]
            指定されたcountyを保持するcity
            （引数なしの場合は'county'を保持
            するすべてのcity）

        '''

        if county in self.county_city:
            return self.county_city[county]
        elif county == 'All':

            #1次元配列に変換
            onedarray=[] # type: List[City]
            for cityList in self.county_city.values() :
                if len(cityList) == 1:
                    onedarray.append(cityList[0])
                else:
                    for city in cityList:
                        onedarray.append(city)
            return onedarray

        else:
            raise ValueError("County value is invalid.")

    def get_county_all(self):
        '''cityオブジェクトが持つすべてのcountyを取得

        このオブジェクトで管理されているcityオブジェクト
        が保持するcountyを返却する．

        Returns
        -------
        self.county_city.values() : List[City]
            cityオブジェクトが保持するcounty_cityのリスト

        '''
        return self.county_city.keys()
    
    def isCounty(self, county:str)->bool:
        '''引数のcountyを持つcityオブジェクトの存在確認

        citySetオブジェクトに属しているcityオブジェクト
        に引き数に該当するcountyが存在するかどうかの確認

        '''
        if county in self.county_city:
            return True
        else:
            return False        

    def get_from_order(self, order:int)->City:
        '''色指標の順番からcityオブジェクトを取得

        Parameters
        ----------
        order : int
            取得したいCityオブジェクトの色指標
        
        Returns
        -------
        City
            orderに対応するCityオブジェクト

        '''

        if(order<len(self.order_city)):
            return  self.order_city[order]
        else:
            raise ValueError("Order value is invalid.")
    
    def get_from_colorcode(self, colorcode:str)->City:
        '''カラーコードから対応するCityオブジェクトを取得
        
        Parameters
        ----------
        colorcode : str
            取得したいCityオブジェクトのカラーコード

        Returns
        -------
            colorcodeに対応するCityオブジェクト
        
        '''

        if colorcode in self.colorcode_city:
            return self.colorcode_city[colorcode]
        else:
            raise ValueError("ColorCode value is invalid.")



