import pyper
import os

#create R object
r = pyper.R()

#import R library
r("source(file='R/library_import.R')")

#input shapefile
shapefile = 'data/N03-200101_27_GML/N03-20_27_200101.shp'
r.assign('shapefile',shapefile)

#make tmporary directory.
os.makedirs('./tmp',exist_ok=True)

#set output svg file name
svgfile = './tmp/OsakaMap.png'
r.assign('svgfile',svgfile)



#output OsakaMap
#Each area are colored according to municipality code.
r('shp <- sf::st_read(shapefile,options="ENCODING=UTF-8")')
#r('png(svgfile, width=25, height=12)')
r('png(svgfile, width=500, height=500)')
r('ggplot()+geom_sf(data=shp,aes(fill=N03_007))')
r('dev.off()')
