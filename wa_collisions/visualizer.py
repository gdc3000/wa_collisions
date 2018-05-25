"""
Functions to visualize data.

Each function excepts the data in form of a
dataframe and creates a visualization.
"""

import folium
import numpy as np

MAP_JSON_DEFAULT = "wa_collisions/data/Neighborhoods/Neighborhoods.json"
MAP_LOCATION_START = [47.6199206, -122.3230027]
MAP_ZOOM = 11
ERROR = 0.000001


def visualize_neighborhood(neighborhood_data, mapping_value, path=None):
    """
    Visualizes the data provided per neighborhood in abs
    folim map and returns the map.

    Args:
        neighborhood_data(pandas dataframe): Dataframe containing
            the data value per neighborhood which is to be mapped.
        mapping_value (string): Name of column of neighborhood_data
            to be mapped.
        path (string): path the geo json file of neighborhoods.

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

    if path is None:
        path = MAP_JSON_DEFAULT

    neigborhood_map = folium.Map(
        location=MAP_LOCATION_START,
        zoom_start=MAP_ZOOM)

    # Finding maximum and minimum values for range
    # Adding a small error to max as folium is not good at comparing floats
    max_value = max(neighborhood_data[mapping_value]) + ERROR
    min_value = min(neighborhood_data[mapping_value])

    neigborhood_map.choropleth(
        geo_data=path,
        data=neighborhood_data,
        columns=['object_id', mapping_value],
        key_on='feature.properties.OBJECTID',
        threshold_scale=list(np.linspace(min_value, max_value, 6)),
        fill_color='YlOrRd',
        highlight=True)
    return neigborhood_map

def visualize_neighborhood_count(neighborhood_data, path=None):
    """
    Visualizes the number of rows per each neighborhood.

    Args:
        neighborhood_data(pandas dataframe): Dataframe containing
            the rows per neighborhood which is to be mapped.
        path (string): path the geo json file of neighborhoods.

    Returns:
        the map produced

    Raises:
        ValueError: if neighborhood_data doesn't have the column
            'object_id' denoting neighborhood.
    """
    if not 'object_id' in neighborhood_data.columns:
        raise ValueError("Dataframe doesn't have a column object_id")
    counts_per_neighborhood = neighborhood_data.groupby(
        ['object_id']).size().reset_index(name='count')
    return visualize_neighborhood(counts_per_neighborhood, 'count', path)

def visualize_neighborhood_mean(neighborhood_data, value, path=None):
    """
    Visualizes the mean value for each neighborhood.

    Args:
        neighborhood_data(pandas dataframe): Dataframe containing
            the rows per neighborhood which is to be mapped.
        value (string): Name of column of neighborhood_data
            whose mean value is to be calculated and mapped.
        path (string): path the geo json file of neighborhoods.

    Returns:
        the map produced

    Raises:
        ValueError: if neighborhood_data doesn't have the column
            'object_id' denoting neighborhood or the column value.
    """
    if not 'object_id' in neighborhood_data.columns:
        raise ValueError("Dataframe doesn't have a column object_id")
    if not value in neighborhood_data.columns:
        raise ValueError("Dataframe doesn't have a column " + value)
    counts_per_neighborhood = neighborhood_data.groupby(
        ['object_id'])[value].mean().reset_index(name='mean')
    return visualize_neighborhood(counts_per_neighborhood, 'mean', path)
