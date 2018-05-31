"""
Function to read the neighborhood data for Seattle
and assign it to collisions.

This file reads the geojson file and provides an interface which
given a dataframe containing latitudes and longitudes, assigns
Seattle neighbourhoods to them
"""

import geopandas as gpd
import numpy as np
from shapely.geometry import Point

def get_neighborhood(latitude, longitude, neighborhoods):
    """
    Returns the Object ID for the Seattle neighborhood for a
    given latitude and longitude.

    Returns -1 if the location is not in any Seattle
    neighborhood

    Args:
        latitude (float): latitude of the location
        longitude (float): longitude of the location
        neighborhoods (geopandas dataframe): neighborhoods

    Returns:
        object_id (int): object id of the seattle
        neighborhood. object_id varies from 1 to 119
        (inclusive). Returns -1 if the location is not
        in any Seattle neighborhood.

    Raises:
        ValueError: if the latitude or longitude can't be
            converted into float
    """
    neighborhood_count = _find_neighborhood_count(neighborhoods)

    location_point = Point(float(latitude), float(longitude))
    for i in range(0, neighborhood_count):
        if neighborhoods['geometry'][i].contains(location_point):
            return neighborhoods['OBJECTID'][i]
    return -1


def assign_neighborhood(dataframe, path=None):
    """
    Returns the provided dataframe with an additional column
    object_id which contains the object id of the seattle
    neighborhood of the location in the dataframe.

    The dataframe must have columns X and Y for the location.

    Args:
        dataframe(pandas dataframe): dataframe containing the
            locations in seattle. Must have columns X and Y

    Returns:
        dataframe(pandas dataframe): the provided dataframe with an
            added column "object_id" containing the object id of the
            neighborhood in seattle the location is present in. If the
            location is in't any of the neighborhood, the column
            contains the value -1.

    Raises:
        ValueError: if the dataframe doesn't contain the columns
            X or Y.
        ValueError: if the X or Y can't be
            converted into float
    """
    if not 'X' in dataframe.columns:
        raise ValueError("Dataframe doesn't have a column X")
    if not 'Y' in dataframe.columns:
        raise ValueError("Dataframe doesn't have a column Y")

    neighborhoods = pull_neighborhoods_file(path)
    object_ids = np.zeros(len(dataframe))
    for i, _ in enumerate(object_ids):
        object_ids[i] = get_neighborhood(
            dataframe['X'][i], dataframe['Y'][i], neighborhoods)

    dataframe['object_id'] = object_ids
    return dataframe

def pull_neighborhoods_file(path=None):
    """
    Read GeoJson file of Neighborhoods.

    Args:
        path(string): path to geojson file.
    Returns:
        GeoJson data frame of neighborhoods.
    """
    if path is None:
        path = 'wa_collisions/data/Neighborhoods/Neighborhoods.json'
    return gpd.read_file(path)

def _find_neighborhood_count(frame=None, path=None):
    if frame is None:
        frame = pull_neighborhoods_file(path)
    return len(frame)
