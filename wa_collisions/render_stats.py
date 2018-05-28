"""
Render stats functions

Module contains functions which are used to pull, clean-up data and run a
causal impact analysis on whether or not trends in collisions changed
measurably after speed limits were reduced in central Seattle in
October 2016.
"""

# import packages
import os
from datetime import datetime
import geopandas

import wa_collisions.read_clean_integrate_data as read_clean_integrate_data

VALID_RESAMPLE_TYPES = ['M', 'W', 'D']

# added in because of change to read_clean_integrate_data
GEO_PATH = "wa_collisions/data/Neighborhoods/Neighborhoods.json"

def read_collision_with_neighborhoods(file_path, contains_neighborhood=False):
    """
    Read in the collision dataframe.

    Uses the input file path to find the csv file with the collision
    data from Washington state.

    Args:
        file_path: the path to the .csv file containing the collision data
        contains_neighborhood: if a file which already has the neighborhood
            object_ids is available at the file path, then this arg should
            be set to true. This will reduce the processing time
            significantly.

    Returns:
        dataframe of data from the collision data file and containing
            an extra column 'object_id' which refers to id of the
            neighbhorhood the collision occurred in.

    Raises:
        ValueError: raises this error when the file path does not exist
    """

    data = read_clean_integrate_data.read_collision_data(file_path)

    if contains_neighborhood and 'object_id' not in data.columns:
        raise ValueError("frame created from {0} does not contain a \
            a field called 'object_id' which is the id for the \
            neighborhood.".format(file_path))

    if not contains_neighborhood:
        data = read_clean_integrate_data.clean_collisions_neighborhoods(data, GEO_PATH)
    else:
        data = read_clean_integrate_data.clean_collision_data(data)

    return data

def pivot_by_treatment(input_frame, treatment_list, control_list=None
                       , neighborhood_path='wa_collisions/data/Neighborhoods/Neighborhoods.json'
                       , agg_by=None, resample_by='D'):
    """
    Read in the collision dataframe with a neighborhood assigned.

    Uses the input file path to find the csv file with the collision
    data from Washington state.

    Args:
        input_frame: the dataframe containing the collision data
        treatment_list: a list containing the names of the neighborhoods
            in the treatment group. For the purpose of this study, this
            is neighborhoods where the speed limit changed.
        control_list (default = None): a list containing the names of the
            neighborhoods in the control group. If None is passed, then
            neighborhoods not in the treatment list are assumed to be
            in the control list.
        neighborhood_path (default = '../wa_collisions/data
            /Neighborhoods/Neighborhoods.json'): a path to the json
            file which contains the Seattle neighborhoods and can
            be used to map object_id to a neighbhorhood name.
        agg_by (default = None): tells the function which
            field in the input frame to aggregate the data by. If None
            is passed, then the function will default to a count of rows,
            otherwise the data will sum the given field.
        resample_by (default = 'D'): tells the function which
            level the data will be grouped by. Acceptable values
            are 'D','W','M', for day, week, and month
            respectively.

    Returns:
        dataframe of data from the collision data file with day

    Raises:
        ValueError: raises this error when the dataframe does not contain
            a column called 'object_id'.
        ValueError: raises this error when neighborhood_path is not a valid
            path.
        ValueError: raises this error when resample_by does not contain
            either 'D','W' or 'M'.
        ValueError: raises this error when agg_by is not None or a string.
    """

    if 'object_id' not in input_frame.columns:
        raise ValueError("input_frame does not contain the id of the \
            neighborhood, called 'object_id'. Please add this field.")

    if not os.path.exists(neighborhood_path):
        raise ValueError("neighborhood_path doesn't exist: " + str(neighborhood_path))
    
    if resample_by not in VALID_RESAMPLE_TYPES:
        raise ValueError("Parameter resample_by must be one of: " \
            + str(VALID_RESAMPLE_TYPES))

    if not isinstance(agg_by, str) and agg_by is not None:
        raise ValueError("agg_by must be either None or of type string.")

    if agg_by not in input_frame.columns and agg_by is not None:
        raise ValueError("agg_by must be either None or a valid column")

    data = input_frame.copy()

    neighborhoods_df = geopandas.read_file(neighborhood_path)
    
    #Find treatment groups by id
    treatment_ids = _find_neighborhoods_ids(input_list=treatment_list
                                            , neighborhoods_df=neighborhoods_df)

    #Find control group
    if control_list is None or control_list == []:
        control_ids = list(set(neighborhoods_df['OBJECTID'].unique()) - set(treatment_ids))
    else:
        control_ids = _find_neighborhoods_ids(input_list=control_list
                                              , neighborhoods_df=neighborhoods_df)

    #Filter data
    data = data[data['object_id'].isin(treatment_ids) | data['object_id'].isin(control_ids)]

    #Add speed limit change
    data['speedlimit_change_flag'] = data['object_id'].isin(treatment_ids)

    #Pivot data
    if agg_by is None:
        data = data.groupby(['time', 'speedlimit_change_flag']).size()
    else:
        data = data.groupby(['time', 'speedlimit_change_flag'])[agg_by].sum()

    data = data.unstack()
    data = data.fillna(0)
    data = data.rename(columns={True: "SpeedLimitChange", False: "SpeedLimitSame"})  
    data = data[['SpeedLimitChange', 'SpeedLimitSame']]

    #Resample data
    return data.resample(resample_by).sum()

def find_period_ranges(input_frame, transition_date="2016-10-01"):
    """
    Read in the input_frame dataframe which is the frame returned
    by pivot_by_treatment.

    Based on this frame and a transition date, this function finds
    the start and end dates of the pre and post transition date
    periods. In the cases where the dates in the frame represents
    weeks or months and do not match the transition date exactly,
    the function will draw the boundary based on which dates are
    closest.

    Args:
        input_frame: the dataframe containing the collision data
        transition_date: date when the pre-period ends and the post
            period begins. Should be a string in the format of 
            'YYYY-MM-DD'.

    Returns:
        a list of 2 lists with 2 elements. List 1 is the date range
        of the pre-period. List 2 is the date range of the post-period.

    Raises:
        ValueError: raises this error when the transition date comes
            before the min date of the given frame or after the max
            date of the given frame.
    """
    min_date = input_frame.index.min()
    max_date = input_frame.index.max()

    transition_datetime = datetime.strptime(transition_date, '%Y-%m-%d')
    if transition_datetime <= min_date or transition_datetime >= max_date:
        raise ValueError("transition_date {0} must be between the minimum \
                         and maximum frame dates.".format(transition_date))

    actual_transition = input_frame.ix[input_frame.index.
                                       get_loc(transition_datetime, method='nearest')].name

    if actual_transition < transition_datetime:
        pre_end = actual_transition
        post_start = input_frame.ix[input_frame.index.
                                    get_loc(transition_datetime, method='nearest')+1].name
    else:
        pre_end = input_frame.ix[input_frame.index.
                                 get_loc(transition_datetime, method='nearest')-1].name
        post_start = actual_transition

    pre_period_range = [min_date.strftime('%Y-%m-%d'), pre_end.strftime('%Y-%m-%d')]
    post_period_range = [post_start.strftime('%Y-%m-%d'), max_date.strftime('%Y-%m-%d')]

    return [pre_period_range, post_period_range]     

def _find_neighborhoods_ids(input_list, neighborhoods_df):
    """
    Read in a list of names of neighborhood names. Returns a list of
    neighbhorhood ids

    Args:
        input_list: a list containing the names of the neighborhoods
            in the treatment group.
        neighborhoods_df: a dataframe containing neighborhood names
            and object_id for each neighborhood.

    Returns:
        a list of neighborhood ids corresponding wiht the given names.

    """

    id_list = []
    for i in range(0, len(input_list)):
        id_list = id_list + \
            [int(neighborhoods_df[neighborhoods_df['S_HOOD'] == input_list[i]]['OBJECTID'])]

    return id_list
