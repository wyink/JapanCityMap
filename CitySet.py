import copy

class CitySet:
    pathnum_city  = {} #area->city
    order_city    = {} #order->city
    citycode_city = {} #citycode->city

    def __init__(self,CityList):
        self.cityList = CityList

        #init
        dict_to_city = self.key_to_city()
        pathnum_city = dict_to_city[0]
        order_city = dict_to_city[1]
        citycode_city = dict_to_city[2]
    
    def key_to_city(self):
        pathnum_city = {} 
        for city in self.cityList:
            for pathnum in city.areablocks_getter():
                pathnum_city[pathnum] = copy.copy(city)

            for citycode in city.citycode_getter():
                citycode_city[citycode] = copy.copy(city)
            
            for prefec in city.prefec_getter():
                prefec_city[prefec] = copy.copy(city)

            for branch in city.branch_getter():
                branch_city[prefec] = copy.copy(city)

            for county in city.county_getter():
                county_city[prefec] = copy.copy(city)

            for cityname in city.cityname_getter():
                cityname_city[cityname] = copy.copy(city)
            
            for order in city.order_getter() :
                order_city[order] = copy.copy(city)

            for colorcode in city.colorcode_getter() :
                colorcode_city[colorcode] = copy.copy(city)
            
        return pathnum_city,order_city,citycode_city
    
    
    
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
    
        