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

from wa_collisions.neighborhood_reader import assign_neighborhood

def read_collision_data(file_path):
    """
    Read in the collision dataframe.

    Uses the input file path to find the csv file with the collision
    data from Washington state.


    Args:
        file_path: the path to the .csv file containing the collision data

    Returns:
        dataframe of data from the collision data file

    Raises:
        ValueError: raises this error when the file path does not exist
    """
    # check that the file exists
    # adapted from 07-Exceptions
    if not os.path.exists(file_path):
        raise ValueError("file doesn't exist: " + str(file_path))

    # read in the data frome the file
    collision_data = pd.read_csv(file_path)

    # return the data
    return collision_data

def read_weather_data(file_path):
    """
    Read in the weather data.

    Uses the input file path to ...


    Args:
        file_path: the path to the .csv file containing the weather data

    Returns:
        dataframe of data from the weather data file

    Raises:
        ValueError: raises this error when the file path does not exist
    """
    # check that the file exists
    # adapted from 07-Exceptions
    if not os.path.exists(file_path):
        raise ValueError("file doesn't exist: " + str(file_path))

    # read in the data frome the file
    weather_data = pd.read_csv(file_path, low_memory = False)

    # return the data
    return weather_data


def clean_collision_data(collision_data,include_since_year=None):
    """
    Clean the collision data.

    Uses the collision data and returns a cleaned data frame ...


    Args:
        data:

    Returns:
        cleaned dataframe of data from the collision data file

    Raises:
        None
    """
    # change the dates to date time and extract year, month, day, hour
    # for joining with weather data later
    # edited this because dt.year has a Future warning
    # edited so that we use the ['new_column'] instead of .new_column
    # for creating a new column
    # reference:
    # https://pandas.pydata.org/pandas-docs/stable/
    # indexing.html#attribute-access

    # convert the column names to lower case
    # in between downloading the data and submitting the project, the file
    # changed
    collision_data.columns = [c.lower() for c in collision_data.columns]
    collision_data = collision_data.rename(columns = {'x':'X', 'y':'Y'})

    if not isinstance(include_since_year, int) and include_since_year is not None:
        raise ValueError("{0} is not None or an int".format(include_since_year))

    collision_data['time'] = pd.to_datetime(collision_data.incdttm)
    collision_data['year'] = collision_data.time.dt.year
    collision_data['month'] = collision_data.time.dt.month
    collision_data['day'] = collision_data.time.dt.day

    # only keep attributes that are relevant to the analysis
    columns = ['Y', 'X', 'addrtype', 'collisiontype', 'fatalities', 'injuries',
               'lightcond', 'roadcond', 'junctiontype', 'location',
               'pedcount', 'pedcylcount', 'personcount', 'sdot_coldesc',
               'severitydesc', 'speeding', 'weather', 'time',
               'year', 'month', 'day', 'S_HOOD']

    # Handle exception where neighborhood is included
    if 'object_id' in collision_data.columns:
        columns = columns + ['object_id']

    # recieving a warning about using .loc
    #collision_data.loc[(-collision_data.X.isna()) & (-collision_data.Y.isna() &
    # (collision_data.year >= 2014)), columns]
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

    return collision_data


def clean_weather_data(weather_data):
    """
    Clean the weather data.

    Uses the weather data and returns a cleaned data frame ...


    Args:
        data:

    Returns:
        cleaned dataframe of data from the collision data file

    Raises:
        None
    """
    # only keep relevant attributes
    columns = ['station', 'valid', 'tmpf', ' p01i', ' sknt']

    #Remove fields with missing values
    weather_data = weather_data.reindex(columns = columns)
    weather_data = weather_data[ (weather_data['tmpf'] != 'M')
                            & (weather_data[' p01i'] != 'M')
                            & (weather_data[' sknt'] != 'M')
                    ]
    weather_data.columns = ['station', 'timestamp','temperature','precipitation','wind_speed']

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
    weather_final_hour = weather_data.groupby(['year','month','day','hour']).agg({'temperature': np.mean,
                                                          'precipitation': np.mean,
                                                          'wind_speed': np.mean}).reset_index()

    # aggregate by day
    weather_final_day = weather_final_hour.groupby(['year','month','day']).agg(
                                                            {'temperature': [np.mean, np.max, np.min],
                                                            'precipitation': np.sum,
                                                            'hour' : np.size,
                                                            'wind_speed': np.mean}).reset_index()
    weather_final_day.columns = weather_final_day.columns.get_level_values(0)
    weather_final_day.columns = ['year','month','day','temperature_mean','temperature_high'
                                ,'temperature_low','precipitation','count_of_obs','wind_speed']

    # only keep days with more than 22 hours of weather data
    weather_final_day = weather_final_day[weather_final_day['count_of_obs'] >= 22]
    weather_final_day = weather_final_day.drop(columns = ['count_of_obs'], axis = 0, inplace = True)

    # return the weather data aggregate at day level
    return weather_final_day



def integrate_data(collision_data_file_path, include_since_year, weather_data_file_path, geo_json_path = None):
    """
    Add the neighborhoods and clean collision data.

    Clean the collision data and add the neighborhood data. We have tests
    for the clean_collision_data and assign neighborhood. We do not have a set
    test for this function because of the run time to assign the neighborhoods.


    Args:
        collision_data_file_path: file path to the collision dataset
        include_since_year:
        weather_data_file_path: file path to the weather dataset
        geo_json_path: file path to the neighorhoods geojson file

    Returns:
        cleaned dataframe of data from the collision data file

    Raises:
        None
    """

    collision_data = read_collision_data(collision_data_file_path)
    collision_data = clean_collision_data(collision_data, include_since_year)

    ## add the assigned neighborhoods
    data = assign_neighborhood(collision_data, geo_json_path)
    if geo_json_path is not None:
        collision_data = assign_neighborhood(collision_data, geo_json_path)

    weather_data = read_weather_data(weather_data_file_path)
    weather_data = clean_weather_data(weather_data)

    # join add weather information
    data = pd.merge(data, weather_data, how = 'inner', on = ['year', 'month', 'day'])

    return data

