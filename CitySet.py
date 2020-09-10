from collections import defaultdict
from typing import List
import City

class CitySet:

    def __init__(self,CityList):
        self.cityList = CityList

        self.pathnum_city   = defaultdict(list) 
        self.citycode_city  = defaultdict(list)  
        self.prefec_city    = defaultdict(list) 
        self.branch_city    = {} 
        self.county_city    = {} 
        self.cityname_city  = {} 
        self.order_city     = {}  
        self.colorcode_city = {}  

        self.unique_attr_getter()
    

    def unique_attr_getter(self):
        '''Cityの各属性値とそれに対応するインスタンスを連携

        Cityの各属性値には複数の値が存在する．場合によって
        該当属性値を保持するcityインスタンス（コンストラクタ
        で代入されるCityListに含まれるうち）が必要になる．
        そのような場合に備えそれぞれの各属性ごとに辞書を作成
        する．

        一つの属性値に対して複数のcityインスタンスが存在する
        場合はリストで保存する．

        '''

        for city in self.cityList:

            for pathnum in city.areablocks():
                self.pathnum_city[pathnum].append(city)

            self.citycode_city[city.citycode]  = city
            self.prefec_city[city.prefec]           .append(city)
            self.cityname_city[city.cityname]       = city         
            self.order_city[city.order]             = city    
            self.colorcode_city[city.colorcode]     = city

            #存在しない場合
            if city.branch !='' :
                self.branch_city[city.branch].append(city)
            
            if city.county !='' :
                self.county_city[city.county] = city

    
    def get_city_from_pathnum(self,pathNum):
        '''入力のpathNumに対応するcityインスタンスを返却

        Parameters
        ----------
        pathNum : int
            入力のsvgの<path>の出現順序
            特定のエリアと対応している．

        Returns
        -------
        pathnum_city[pathNum] : List[City]
            pathNum番目のsvgタグに対応するエリアのcity

        '''

        if (pathNum<len(self.pathnum_city)):
            return self.pathnum_city[pathNum]
        else:
            print("PathNum value is invalid.")

    
    def get_pathnum_all(self):
        '''cityオブジェクトが持つすべてのpathnum

        このオブジェクトで管理されているcityオブジェクト
        が保持するpathnumを返却する．

        Returns
        -------
        self.pathnum_city.keys() : List[int]
            cityオブジェクトが保持するpathnumのリスト

        '''
        return self.pathnum_city.keys()

    def get_city_from_citycode(self,citycode):
        if citycode in self.citycode_city:
            return self.citycode_city[citycode]
        else:
            print("CityCode value is invalid.")


    def get_citycode_all(self):
        '''cityオブジェクトが持つすべてのcitycodeを取得

        このオブジェクトで管理されているcityオブジェクト
        が保持するcitycodeを返却する．

        Returns
        -------
        self.citycode_city.keys() : List[str]
            cityオブジェクトが保持するcitycodeのリスト

        '''
        return self.citycode_city.keys()

    def get_city_from_prefec(self,prefec):
        if prefec in self.prefec_city[prefec]:
            return self.prefec_city[prefec]
        else:
            print("Prefec value is invalid. ")
            
    def get_city_from_branch(self,branch):
        '''

        Returns
        -------
        self.branch_city[branch] : List[City]
        '''
        if branch in self.branch_city[branch]:
            return self.branch_city[branch]
        else:
            print("Branch value is invalid. ")
            
    def get_city_from_county(self,county='All'):
        '''countyを保持するcityを返却する

        引数にcountyを指定した場合は該当するcounty
        を保持するcityを返却する．
        引数なしで呼び出された場合はcountyを保持する
        すべてのcityを返却する．（cityオブジェクトは
        必ずしもcountyを保持しないため利用されえる．）

        Parameters
        ----------
        county : str
            群・および政令都市名

        Returns
        -------
        List[City]
            指定されたcountyを保持するcity
            （引数なしの場合は'county'を保持するすべてのcity）

        '''
        if county in self.county_city:
            return self.county_city[county]
        elif county == 'All':
            return self.county_city.values()
        else:
            print("County value is invalid. ")

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


    def get_from_order(self,order):
        if(order<len(self.order_city)):
            return  self.order_city[order]
        else:
            print("Order value is invalid.")
    
    def get_from_colorcode(self,colorcode):
        if colorcode in self.colorcode_city[colorcode]:
            return self.colorcode_city[colorcode]
        else:
            print("ColorCode value is invalid. ")




city = City.City(27,["osaka","","sakai","yao"],[2,3,4],4)
city2 = City.City(7,["osaka","","oosaka","kashiwara"],[1],2)
c = CitySet([city,city2])

a = c.get_city_from_county()
for i in a :
    print(i.cityname)


