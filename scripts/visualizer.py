"""
Functions to visualize data.

Each function excepts the data in form of a
dataframe and creates a visualization.
"""

import folium
import numpy as np

MAP_JSON = "../wa_collisions/data/Neighborhoods/Neighborhoods.json"
MAP_LOCATION_START = [47.6199206, -122.3230027]
MAP_ZOOM = 11
ERROR = 0.000001


def visualize_neighborhood(neighborhood_data, mapping_value):
    """
    Visualizes the data provided per neighborhood in abs
    folim map nad returns the map.

    Args:
        neighborhood_data(pandas dataframe): Dataframe containing
            the data value per neighborhood which is to be mapped.
        mapping_value (string): Name of column of neighborhood_data
            to be mapped.

    Returns:
        the map produced

    Raises:
        ValueError: if neighborhood_data doesn't have the column
            'object_id' or mapping_value
    """
    if not 'object_id' in neighborhood_data.columns:
        raise ValueError("Dataframe doesn't have a column object_id")
    if not mapping_value in neighborhood_data.columns:
        raise ValueError("Dataframe doesn't have a column " + mapping_value)

    neigborhood_map = folium.Map(
        location=MAP_LOCATION_START,
        zoom_start=MAP_ZOOM)

    # Finding maximum and minimum values for range
    # Adding a small error to max as folium is not good at comparing floats
    max_value = max(neighborhood_data[mapping_value]) + ERROR
    min_value = min(neighborhood_data[mapping_value])

    neigborhood_map.choropleth(
        geo_data=MAP_JSON,
        data=neighborhood_data,
        columns=['object_id', mapping_value],
        key_on='feature.properties.OBJECTID',
        threshold_scale=list(np.linspace(min_value, max_value, 6)),
        fill_color='YlOrRd',
        highlight=True)
    return neigborhood_map
