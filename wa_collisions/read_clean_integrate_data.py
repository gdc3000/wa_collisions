"""Read, Clean, and Integrate data. 

   Module to read, clean and integrate the data from the weather 
   and collision data sets. 
"""

# import packages
import pandas as pd

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
    data = None

    # return the data 
    return data

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

def clean_collision_data(data):
    """ Clean the collision data.

    Uses the collision data and returns a cleaned data frame ...


    Args:
        data: 

    Returns:
        cleaned dataframe of data from the collision data file

    Raises:
        None
    """
    pass