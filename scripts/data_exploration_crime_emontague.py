## Script to map collisions to beats
## The collisions need to be mapped to beats in order to compare to crime data
## Takes a long time to run 
## Currently only looks at 5 collisions 

## Data from:
## Collisions: https://data-seattlecitygis.opendata.arcgis.com/datasets/collisions/data?geometry=-122.526%2C47.676%2C-122.198%2C47.717
## Beat Shape Files: https://data.seattle.gov/Public-Safety/Seattle-Police-Department-Beats/nnxn-434b
## Crime Data (911): https://data.seattle.gov/Public-Safety/Crime-Data/4fs7-3vj5

import numpy as np
import pandas as pd

import fiona
import shapely
import shapely.geometry

# method from: https://stackoverflow.com/questions/7861196/check-if-a-geopoint-with-latitude-and-longitude-is-within-a-shapefile


# read in the shape file 
beats = fiona.open('SPD_Beats_WGS84/SPD_Beats_WGS84.shp')

# read in the crash data
collisions = pd.read_csv("Collisions.csv")

#iters = collisions.shape[0]
iters = 5

beats = list()

for r in range(0,iters):
    print(r)
    point = shapely.geometry.Point(collisions.loc[r,'X'], collisions.loc[r,'Y'])
    beat_missing = True 
    beat_found = -1
    while(beat_missing):
        for beat_layer in beats:
            beat_num = beat_layer['properties']['beat']
            beat_shape = shapely.geometry.asShape(beat_layer['geometry'])
            if beat_shape.contains(point):
                beat_missing = False
                beat_found = beat_num
    beats.append(beat_found)

print(beats)