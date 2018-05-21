"""Read, Clean, and Integrate data. 

   Module to read, clean and integrate the data from the weather 
   and collision data sets. 
"""

# import packages
import pandas as pd
import os

from wa_collisions.neighborhood_reader import assign_neighborhood

def read_collision_data(file_path):
    """ Read in the collision dataframe.

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
    """ Read in the weather data.

    Uses the input file path to ...


    Args:
        file_path:

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

def clean_collision_data(collision_data):
    """ Clean the collision data.

    Uses the collision data and returns a cleaned data frame ...


    Args:
        data:

    Returns:
        cleaned dataframe of data from the collision data file

    Raises:
        None
    """

    # change the dates to date time 
    # adapted from Fei's exploration notebook 
    collision_data.incdttm = pd.to_datetime(collision_data.incdttm)
    collision_data.incdate = pd.to_datetime(collision_data.incdate)

    return(collision_data)

def add_neighborhoods_collisions(collision_data):
    """ Add the neighborhoods to the cleaned collision data.

    Uses the cleaned collision data and returns a data frame with neighborhoods ...


    Args:
        data:

    Returns:
        cleaned dataframe of data from the collision data file

    Raises:
        None
    """

    ## add the assigned neighborhoods
    # removed for testing - issue because of time to test
    collision_data = assign_neighborhood(collision_data)

    return(collision_data)
    