"""
Function to render a heat map of collisions in Seattle based on user-input filters 

"""

import pandas as pd
import numpy as np
from IPython.display import display
import ipywidgets as widgets
from ipywidgets import interactive

import folium
import folium.plugins as plugins
from folium.plugins import HeatMap

# Read in data -- to be replace with calling the read_clean_integrate_data module
df = pd.read_csv("../../project_datasets/Collisions_weather_iem_day_2014_2018_fei.csv")


# Define widget
weather_selection = widgets.Dropdown(
    options=list(set(df[-pd.isnull(df.weather)].weather.values)),
    value='Snowing',
    description='Weather:',
    disabled=False
)

columns = ['X', 'Y', 'weather']

# Define function to view or plot data
def map_by_weather(weather=''):
    df_collision = df.loc[df.weather == weather, columns].dropna(axis = 0, how = 'any')
    coordinates = df_collision.loc[:, ['Y', 'X']].values
    NewData = coordinates * np.array([[1, 1]])
    
    data = list()
    data.append(NewData.tolist())
    m = folium.Map(location=[47.706850, -122.333961], 
                   tiles='Stamen Toner', 
                   zoom_start=11)
    HeatMap(data[0]).add_to(m)
    display(m)
    
# Define interactivity
interactive(map_by_weather, weather=weather_selection)