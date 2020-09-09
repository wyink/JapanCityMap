from collections import defaultdict
from typing import List
import City

class CitySet:

    def __init__(self,CityList):
        self.cityList = CityList
        self.pathnum_city   = defaultdict(list)  
        self.citycode_city  = defaultdict(list)  
        self.prefec_city    = defaultdict(list) 
        self.branch_city    = defaultdict(list) 
        self.county_city    = defaultdict(list) 
        self.cityname_city  = defaultdict(list) 
        self.order_city     = defaultdict(list)  
        self.colorcode_city = defaultdict(list)  

        #init
        self.key_to_city()
    
    def key_to_city(self):
        '''Cityの各属性値とそれに対応するインスタンスを連携

        Cityの各属性値には複数の値が存在する．場合によって
        該当属性値を保持するcityインスタンス（コンストラクタ
        で代入されるCityListに含まれるうち）が必要になる．
        そのような場合に備えそれぞれの各属性ごとに辞書を作成
        する．

        '''

        for city in self.cityList:

            for pathnum in city.areablocks:
                self.pathnum_city[pathnum] = city

            self.citycode_city[city.citycode] =defaultdict(list)
            self.citycode_city[city.citycode].append[city]
                    
            self.prefec_city[city.prefec]       = city
            self.branch_city[city.branch]       = city
            self.county_city[city.county]       = city
            self.cityname_city[city.cityname]   = city         
            self.order_city[city.order]         = city
            self.colorcode_city[city.colorcode] = city    
    
    
    def get_from_pathnum(self,pathNum):
        '''入力のpathNumに対応するcityインスタンスを返却

        Parameters
        ----------
        pathNum : int
            入力のsvgの<path>の出現順序
            特定のエリアと対応している．

        Returns
        -------
        pathnum_city[pathNum] : City
            pathNum番目のsvgタグに対応するエリアのcity

        '''

        if (pathNum<len(self.pathnum_city)):
            return self.pathnum_city[pathNum]
        else:
            print("PathNum value is invalid.")

    
    def get_from_pathnum_all(self)->'List[str]':
        '''
        このオブジェクトで管理されているすべてのcityオブジェクト
        からpathNum
        '''

        pass

    def get_from_order(self,order):
        if(order<len(self.order_city)):
            return  self.order_city[order]
        else:
            print("Order value is invalid.")
    
    def get_from_citycode(self,citycode):
        if citycode in citycode_city:
            return citycode_city[citycode]
        else:
            print("CityCode value is invalid.")


'''
city = City.City(27,["osaka","","","yao"],[2,3,4],4)
city2 = City.City(7,["osaka","","","kashiwara"],[1],2)
c = CitySet([city,city2])

'''
