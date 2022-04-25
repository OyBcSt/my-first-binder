#Here is the code from the Jupyter notebook, so it is human readable...I did not actually test it as a standalone script!
import pandas as pd
station_file = "CastFile_0322-OB20220317.csv"
station_data = pd.read_csv(station_file)
#Uncomment to check station_data
#station_data
locations = station_data[['Lat', 'Lon']]
locationlist = locations.values.tolist()
#print(len(locationlist))
#print(locationlist[7])
import branca
import branca.colormap as cm
colormap = cm.LinearColormap(colors=['darkred','red','orange','yellow','green','darkblue','purple'], index=[1,2,3,4,5,6,20],vmin=1,vmax=20)
colormap
# -*- coding: utf-8 -*-
"""
# Name: Visualization of raster in folium 
# Author:      Dai shaoqing
#
# Created:     09/13/2017
# Copyright:   (c) Dai shaoqing <dsq1993qingge@163.com> 2017
#------------------------------------------------------------
"""
#Load library
from osgeo import gdal
import folium
from folium import plugins

#Open raster file
driver=gdal.GetDriverByName('GTiff')
driver.Register() 
ds = gdal.Open('MobileBayElevation.tif') 
if ds is None:
    print('Could not open')

#Get coordinates, cols and rows
geotransform = ds.GetGeoTransform()
cols = ds.RasterXSize 
rows = ds.RasterYSize 

#Get extent
xmin=geotransform[0]
ymax=geotransform[3]
xmax=xmin+cols*geotransform[1]
ymin=ymax+rows*geotransform[5]

#Get Central point
centerx=(xmin+xmax)/2
centery=(ymin+ymax)/2

#Raster convert to array in numpy
bands = ds.RasterCount
band=ds.GetRasterBand(1)
dataset= band.ReadAsArray(0,0,cols,rows)
dataimage=dataset
#dataimage[dataimage[:,:]==-340282346638528859811704183484516925440.000]=0
m = folium.Map(location=[30.50355, -87.98733], zoom_start=9)
folium.raster_layers.ImageOverlay(
    image=dataimage,
    opacity=.4,
#    colormap=lambda x: (x, x, x),
#    colormap=matplotlib.cm.jet,
    bounds=[[ymin, xmin], [ymax, xmax]]
).add_to(m)
for point in range(0, len(locationlist)):
    folium.Marker(locationlist[point], popup=station_data['Station'][point] + "\n" + station_data['Date'][point] + "\n" + station_data['Time'][point],icon=folium.Icon(color="white",icon_color=colormap(station_data['Depth (m)'][point]), icon='tint', angle=0, prefix='fa')).add_to(m)
#ogr2ogr -t_srs EPSG:4326 -f GeoJSON subs1.json subs1.shp
#https://shallowsky.com/blog/mapping/folium-with-shapefiles.html
folium.GeoJson("subs1.json").add_to(m)
folium.GeoJson("outlets1.json").add_to(m)
folium.LayerControl().add_to(m)
m.add_child(colormap)
