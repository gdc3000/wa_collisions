"""
Read, Clean, and Integrate data.

Module to read, clean and integrate the data from the weather
and collision data sets.
"""

# import packages
import os
import pandas as pd
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
    data = None

    # return the data
    return data

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
               'severitydesc', 'speeding', 'weather', 'time', 'epoch',
               'year', 'month', 'day','S_HOOD']
    
    #Handle exception where neighborhood is included
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


def clean_collisions_neighborhoods(collision_data, geo_json_path=None):
    """
    Add the neighborhoods and clean collision data.

    Clean the collision data and add the neighborhood data. We have tests
    for the clean_collision_data and assign neighborhood. We do not have a set
    test for this function because of the run time to assign the neighborhoods.


    Args:
        collision_data():

    Returns:
        cleaned dataframe of data from the collision data file

    Raises:
        None
    """

    collision_data = clean_collision_data(collision_data)

    ## add the assigned neighborhoods
    collision_data = assign_neighborhood(collision_data, geo_json_path)

    return collision_data
    