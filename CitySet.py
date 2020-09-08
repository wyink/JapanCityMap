import copy
import City

class CitySet:

    def __init__(self,CityList):
        self.cityList = CityList
        self.pathnum_city   = {} 
        self.citycode_city  = {} 
        self.prefec_city    = {}
        self.branch_city    = {}
        self.county_city    = {}
        self.cityname_city  = {}
        self.order_city     = {} 
        self.colorcode_city = {} 

        #init
        self.key_to_city()
    
    def key_to_city(self):
        pathnum_city = {} 
        for city in self.cityList:
            for pathnum in city.areablocks_getter():
                self.pathnum_city[pathnum] = copy.copy(city)

            citycode = city.citycode_getter()
            self.citycode_city[citycode] = copy.copy(city)
            
            prefec = city.prefec_getter()
            self.prefec_city[prefec] = copy.copy(city)

            branch = city.branch_getter()
            self.branch_city[prefec] = copy.copy(city)

            county = city.county_getter()
            self.county_city[prefec] = copy.copy(city)

            cityname = city.cityname_getter()
            self.cityname_city[cityname] = copy.copy(city)
            
            order = city.order_getter() 
            self.order_city[order] = copy.copy(city)

            colorcode = city.colorcode_getter() 
            self.colorcode_city[colorcode] = copy.copy(city)
            
    
    
    
    def get_from_pathnum(self,path)->'city-object':
        if (path<len(pathnum_city)):
            return pathnum_city[path]
        else:
            print("PathNum value is invalid.")
    
    def get_from_order(self,order)->'city-object':
        if(order<len(order_city)):
            return  order_city[order]
        else:
            print("Order value is invalid.")
    
    def get_from_citycode(self,citycode):
        if citycode in citycode_city:
            return citycode_city[citycode]
        else:
            print("CityCode value is invalid.")


city = City.City(27,["osaka","","","yao"],[2,3,4],4)
city2 = City.City(7,["osaka","","","kashiwara"],[1],2)
c = CitySet([city,city2])
