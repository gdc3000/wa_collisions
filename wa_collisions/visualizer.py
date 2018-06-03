"""
Functions to visualize data.

Each function excepts the data in form of a
dataframe and creates a visualization.
"""

import pandas as pd
import numpy as np
import folium
import folium.plugins as plugins
import ipywidgets as widgets

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


def visualize_heatmap_with_time(data, start_date='2001-01-01', end_date='2020-01-01'):
    """
    Visualizes the mean value for each neighborhood.

    Args:
        data(pandas dataframe): Dataframe containing
            the rows per collisions which is to be mapped.
        start_date (string): the starting date of the collisions
            to be presented in the heatmap
        end_date (string): the end date of the collisions
            to be presented in the heatmap

    Returns:
        the heatmap produced

    Raises:
        ValueError: if neighborhood_data doesn't have the column
            'object_id' denoting neighborhood or the column value.
    """

    columns = ['Y', 'X', 'date', 'object_id']
    df_collision = data.reindex(columns=columns)
    df_collision = df_collision.dropna(axis=0, how='any')

    dateMask = ((df_collision['date'] >= np.datetime64(start_date)) &
                (df_collision['date'] <= np.datetime64(end_date)))
    index = dateMask
    data_subset = df_collision.reindex(index[index].index.values)
    dates = sorted(data_subset.date.value_counts().index.values)

    data = list()
    for date in dates:
        dateMask = df_collision['date'] == date
        index = dateMask
        coordinates = df_collision.reindex(index[index].index.values)[['Y', 'X']].values
        NewData = coordinates * np.array([[1, 1]])
        data.append(NewData.tolist())

    # create heatmap object
    time_index = [pd.to_datetime(date).strftime('%Y-%m-%d')  for date in dates]

    m = folium.Map(location=MAP_LOCATION_START,
                   zoom_start=MAP_ZOOM)

    hm = plugins.HeatMapWithTime(
        data,
        index=time_index,
        auto_play=True,
        max_opacity=0.3)

    hm.add_to(m)

    return m

def generate_factor_list(factor_list, df):
    """
    TO-DO: add docstring
    """

    factors = dict()
    for _, key in enumerate(factor_list):
        factors[key] = df[key].value_counts().index.values
    return factors

def roadcond_selection_widget(roadcond_list):
    """
    TO-DO: add docstring
    """
    style = {'description_width': 'initial'}
    roadcond_selection = widgets.Dropdown(
        options=roadcond_list,
        value=roadcond_list[0],
        description='Road Condition:',
        style=style,
        disabled=False
    )
    return roadcond_selection

def weather_selection_widget(weather_list):
    """
    TO-DO: add docstring
    """
    style = {'description_width': 'initial'}
    weather_selection = widgets.Dropdown(
        options=weather_list,
        value=weather_list[0],
        description='Weather Type:',
        style=style,
        disabled=False
    )
    return weather_selection


def map_by_roadcond_weather(df, map_json_path, roadcond='', weather=''):
    """
    TO-DO: add docstring
    """
    columns = ['X', 'Y', 'roadcond', 'weather', 'object_id']
    mask = (df.roadcond == roadcond) & (df.weather == weather)
    df_collision = df.loc[mask, columns].dropna(axis=0, how='any')
    if df_collision.shape[0] == 0:
        print("No matched collision")
        return None
    return visualize_neighborhood_count(df_collision, path=map_json_path)


def map_by_roadcond(df, map_json_path, roadcond=''):
    """
    TO-DO: add docstring
    """
    columns = ['X', 'Y', 'roadcond', 'object_id']
    mask = (df.roadcond == roadcond)
    df_collision = df.loc[mask, columns].dropna(axis=0, how='any')
    if df_collision.shape[0] == 0:
        print("No matched collision")
        return None
    return visualize_neighborhood_count(df_collision, path=map_json_path)
