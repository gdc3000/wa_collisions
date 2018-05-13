## Script to map collisions to beats
## Takes a long time to run 
## Currently only looks at 5 collisions 

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