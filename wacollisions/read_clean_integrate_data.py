"""
Read, Clean, and Integrate data.

Module to read, clean and integrate the data from the weather
and collision data sets.
"""

# import packages
import os
import pandas as pd
import numpy as np
#from pytz import timezone

from wacollisions.neighborhood_reader import assign_neighborhood

def read_collision_data(file_path):
    """

    Uses the input file path to find the csv file with the collision
    data from Washington state.


    Args:
        file_path: the path to the .csv file containing the collision data

    Returns:
        dataframe of data from the collision data file

    Raises:
        ValueError: raises this error when the file path does not exist
    """

    if not os.path.exists(file_path):
        raise ValueError("file doesn't exist: " + str(file_path))

    # read in the data frome the file
    collision_data = pd.read_csv(file_path, low_memory=False)

    # return the data
    return collision_data

def read_weather_data(file_path):
    """
    Read in the weather data.

    Uses the input file path to find the csv file with the weather
    data from the Iowa Environmental Mosonet database


    Args:
        file_path: the path to the .csv file containing the weather data

    Returns:
        dataframe of data from the weather data file

    Raises:
        ValueError: raises this error when the file path does not exist
    """
    # check that the file exists
    if not os.path.exists(file_path):
        raise ValueError("file doesn't exist: " + str(file_path))

    # read in the data frome the file
    weather_data = pd.read_csv(file_path, low_memory=False)

    # return the data
    return weather_data


def clean_collision_data(collision_data, include_since_year=None):
    """
    Clean the collision data.

    Uses the collision data and returns a cleaned data frame


    Args:
        data: dataframe that contains the raw data from the collision data file
        include_since_year: the starting year of collision accidents in the output dataframe

    Returns:
        cleaned dataframe of data from the collision data file

    Raises:
        ValueError: raises this error when the user-input year is not an integer
    """

    # convert the column names to lower case
    collision_data.columns = [c.lower() for c in collision_data.columns]
    collision_data = collision_data.rename(columns={'x':'X', 'y':'Y'})

    if not isinstance(include_since_year, int) and include_since_year is not None:
        raise ValueError("{0} is not None or an int".format(include_since_year))

    collision_data['time'] = pd.to_datetime(collision_data.incdttm)
    collision_data['date'] = pd.to_datetime(collision_data.incdate)
    collision_data['year'] = collision_data.time.dt.year
    collision_data['month'] = collision_data.time.dt.month
    collision_data['day'] = collision_data.time.dt.day
    collision_data['hour'] = collision_data.time.dt.hour
    collision_data['minute'] = collision_data.time.dt.minute
    collision_data['second'] = collision_data.time.dt.second

    # only keep attributes that are relevant to the analysis
    columns = ['Y', 'X', 'addrtype', 'collisiontype', 'fatalities', 'injuries',
               'lightcond', 'roadcond', 'junctiontype', 'location',
               'pedcount', 'pedcylcount', 'personcount', 'sdot_coldesc',
               'severitydesc', 'speeding', 'weather', 'time', 'date',
               'year', 'month', 'day', 'hour', 'minute', 'second']

    # Handle exception where neighborhood is included
    if 'object_id' in collision_data.columns:
        columns = columns + ['object_id']

    # drop the na
    collision_data = collision_data.dropna(axis=0, how='any', subset=['X', 'Y'])
    if include_since_year is not None:
        collision_data = collision_data[collision_data.year >= include_since_year]
    collision_data = collision_data.reindex(columns=columns)

    ## add some indicators for later creating the visualizations
    collision_data['ind_ped'] = collision_data.pedcount > 0
    collision_data['ind_speeding'] = collision_data.speeding == 'Y'
    collision_data['ind_person'] = collision_data.personcount > 0
    collision_data['ind_pedcycl'] = collision_data.pedcylcount > 0
    collision_data['ind_fatalities'] = collision_data.fatalities > 0
    collision_data.reset_index(inplace=True)

    # drop redundant columns
    collision_data.drop(columns=['index', 'speeding'], axis=1, inplace=True)

    # remove rows where exact accident time was not available (estimated as start of the date only)
    time_mask = (collision_data.hour != 0) \
                | (collision_data.minute != 0) \
                | (collision_data.second != 0)
    collision_data['ind_valid_time'] = time_mask

    return collision_data


def clean_weather_data(weather_data):
    """
    Clean the weather data.

    Uses the weather data and returns a cleaned data frame


    Args:
        data: dataframe that contains the raw data from the weather data file

    Returns:
        cleaned dataframe of data from the weather data file

    Raises:
        None
    """
    # only keep relevant attributes
    columns = ['station', 'valid', 'tmpf', ' p01i', ' sknt']

    #Remove fields with missing values
    weather_data = weather_data.reindex(columns=columns)
    weather_data = weather_data[(weather_data['tmpf'] != 'M') &
                                (weather_data[' p01i'] != 'M') &
                                (weather_data[' sknt'] != 'M')]
    weather_data.columns = ['station', 'timestamp', 'temperature', 'precipitation', 'wind_speed']

    #convert types to floats
    weather_data['temperature'] = weather_data['temperature'].astype('float64')
    weather_data['precipitation'] = weather_data['precipitation'].astype('float64')
    weather_data['wind_speed'] = weather_data['wind_speed'].astype('float64')

    # convert timestamp attribute from string to datetime format and extract year, month, day
    weather_data['timestamp'] = pd.to_datetime(weather_data['timestamp'])
    weather_data['year'] = weather_data['timestamp'].dt.year
    weather_data['month'] = weather_data['timestamp'].dt.month
    weather_data['day'] = weather_data['timestamp'].dt.day
    weather_data['hour'] = weather_data['timestamp'].dt.hour

    # aggregate by hour
    weather_final_hour = weather_data.groupby(
        ['year', 'month', 'day', 'hour']).agg(
            {'temperature': np.mean,
             'precipitation': np.mean,
             'wind_speed': np.mean}).reset_index()

    # aggregate by day
    weather_final_day = weather_final_hour.groupby(
        ['year', 'month', 'day']).agg(
            {'temperature': [np.mean, np.max, np.min],
             'precipitation': np.sum,
             'hour' : np.size,
             'wind_speed': np.mean}).reset_index()
    weather_final_day.columns = weather_final_day.columns.get_level_values(0)
    weather_final_day.columns = [
        'year',
        'month',
        'day',
        'temperature_mean',
        'temperature_high',
        'temperature_low',
        'precipitation',
        'count_of_obs',
        'wind_speed']

    # only keep days with more than 22 hours of weather data
    weather_final_day = weather_final_day[weather_final_day['count_of_obs'] >= 22]
    weather_final_day.drop(columns=['count_of_obs'], axis=1, inplace=True)

    # return the weather data aggregate at day level
    return weather_final_day



def clean_collisions_neighborhoods(collision_data, geo_json_path=None):
    """
    Add the neighborhoods to the cleaned collision data.
    Clean the collision data and add the neighborhood data. We have tests
    for the clean_collision_data and assign neighborhood. We do not have a set
    test for this function because of the run time to assign the neighborhoods.

    Args:
        collision_data: dataframe that contains the cleaned collision data
        geo_json_path: path to the GeoJSON file that contains neighborhood data
    Returns:
        cleaned dataframe of data from the collision data file with neighborhood attributes
    Raises:
        None
    """

    collision_data = clean_collision_data(collision_data)

    ## add the assigned neighborhoods
    collision_data = assign_neighborhood(collision_data, geo_json_path)

    return collision_data


def integrate_data(
        collision_data_file_path,
        include_since_year,
        weather_data_file_path,
        geo_json_path=None):
    """
    Clean and integrate collision data, weather data and neighborhood data

    Args:
        collision_data_file_path: file path to the collision dataset
        include_since_year: the starting year of collision accidents in the output dataframe
        weather_data_file_path: file path to the weather dataset
        geo_json_path: file path to the neighorhoods GEOJSON file

    Returns:
        cleaned dataframe of data from the integrated data

    Raises:
        ValueError: raises this error when the file paths do not exist
    """

    # read in the collision data
    # check that the file exists
    if not os.path.exists(collision_data_file_path):
        raise ValueError("collision data file doesn't exist: " + str(collision_data_file_path))

    collision_data = read_collision_data(collision_data_file_path)
    collision_data = clean_collision_data(collision_data, include_since_year)

    # add the assigned neighborhoods
    if not os.path.exists(geo_json_path):
        raise ValueError("geo json file doesn't exist: " + str(geo_json_path))
    data = assign_neighborhood(collision_data, geo_json_path)

    # read in the weather data
    if not os.path.exists(weather_data_file_path):
        raise ValueError("weather data file doesn't exist: " + str(weather_data_file_path))
    weather_data = read_weather_data(weather_data_file_path)
    weather_data = clean_weather_data(weather_data)

    # join add weather information
    data = pd.merge(data, weather_data, how='inner', on=['year', 'month', 'day'])

    return data
