# Coding exercise to test the geopandas library. Exercises from the geopandas website
import geopandas,descartes,geoplot
import matplotlib.pyplot as plt
import contextily as ctx
import pandas as pd
from shapely import wkt
#Enable all the test prints
DEBUG = 0

new_data = pd.read_csv('Data/NYGreenInfrastructureAssets.csv')
#Print out to check the data is read correctly
if DEBUG==1: print(" New York Green Infrastructure Data: \n\n", new_data.head(10) , new_data.keys())
# Use the asset area as a way to plot the z axis
new_data_reduced = new_data[['GI_ID', 'Latitude', 'Longitude','Asset_Area']]
# Extracting the lat and long along with GI_ID for a way to keep a unique way to refer
# to the points
if DEBUG==1: print("\n\n Reduced data structure:\n\n", new_data_reduced.head(10))
# Create a tuple of latitude and longitudes
x = list((zip(new_data_reduced.Latitude , new_data_reduced.Longitude)))
y=[]#New empty list
for item in x:
    y.append('POINT(' + str(item[0]) + ' ' +str(item[1]) +')')
#Test print of new tuple column
if DEBUG==1: print("\n\ntype of y: ", type(y) , " first few elements of y: \n", y[0:10])
new_data_reduced['Coordinates'] = pd.Series(y, index = new_data_reduced.index)
del new_data_reduced['Latitude']
del new_data_reduced['Longitude']
del new_data_reduced['GI_ID']
#Test print
if DEBUG==1: print("\n\nAdded Column of the tuple coordinate data:\n" , new_data_reduced.head())
# Now use shapeply.wkt to convert coordinates
new_data_reduced['Coordinates'] = new_data_reduced['Coordinates'].apply(wkt.loads)
#Constructing a geodataframe
gdf = geopandas.GeoDataFrame(new_data_reduced, geometry='Coordinates')
if DEBUG==1: print(" Sample of the geospatial dataframe: \n", gdf.head())




# Convert from pandas data frame to a geopandas dataframe
if DEBUG==1: print(" Boroughs sample :\n\n", boroughs.head() , "\n\n Collisions sample:\n\n" , collisions.head())
new_data_reduced.rename(columns={'Coordinates':'geometry'}, inplace='True')
final_df = geopandas.GeoDataFrame(new_data_reduced)
if DEBUG==0: print ('\n\nType of new data reduced: ',type(final_df)\
     ,'\n\n Newly renamed columns of new_data_reduced :\n\n', final_df.head())
# Now making the geoplot of the plots with the 

#making the heatmap
boroughs = geopandas.read_file(geoplot.datasets.get_path('nyc_boroughs'))
ax = geoplot.kdeplot(
    final_df,# clip=boroughs.geometry,
    shade=True, cmap='Reds', 
    projection=geoplot.crs.WebMercator())
geoplot.polyplot(boroughs, ax=ax, zorder=1)
geoplot.webmap(boroughs,ax=ax,zoom=12)
plt.show()


# Trying to plot as point data over webmap instead of a heat map over a webmap

ax = geoplot.webmap(boroughs, projection=geoplot.crs.WebMercator(), zoom=12)
geoplot.pointplot(final_df[final_df['Asset_Area'] > 10.0 ] , ax=ax)
geoplot.polyplot(boroughs, ax=ax, zorder=1)
plt.show()