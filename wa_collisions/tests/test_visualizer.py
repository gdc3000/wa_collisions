"""
Unittests for visualizer.py
"""

import unittest
import pandas as pd
import folium
import ipywidgets as widgets
from wa_collisions.visualizer import visualize_neighborhood
from wa_collisions.visualizer import visualize_neighborhood_count
from wa_collisions.visualizer import visualize_neighborhood_mean
from wa_collisions.visualizer import visualize_heatmap_by_day
from wa_collisions.visualizer import visualize_heatmap_by_hour
from wa_collisions.visualizer import generate_factor_list
from wa_collisions.visualizer import roadcond_selection_widget
from wa_collisions.visualizer import weather_selection_widget
from wa_collisions.visualizer import district_selection_widget
from wa_collisions.visualizer import map_by_roadcond_weather
from wa_collisions.visualizer import map_by_roadcond
from wa_collisions.read_clean_integrate_data import integrate_data

# store the relative path to the Collisions data, Weather data and GeoJson neighborhoods data
COLLISIONS_DATA = "wa_collisions/data/Collisions_test.csv"
WEATHER_DATA = "wa_collisions/data/Weather_test.csv"
GEO_PATH = "wa_collisions/data/Neighborhoods/Neighborhoods.json"

# Define a class in which the tests will run
class VisualizerTest(unittest.TestCase):
    """
    Unittests for visualizer
    """

    def test_missing_object_id(self):
        """
        Passing a data frame without object id should raise error
        in visualize_neighborhood
        """
        test_data = {"notObjectID": [1], "Value":[2]}
        dataframe = pd.DataFrame(data=test_data)
        with self.assertRaises(ValueError):
            visualize_neighborhood(dataframe, "Value")

    def test_missing_mapping_value(self):
        """
        Passing a data frame without the passed mapping_value
        should raise error in visualize_neighborhood
        """
        test_data = {"object_id": [1], "notValue":[2]}
        dataframe = pd.DataFrame(data=test_data)
        with self.assertRaises(ValueError):
            visualize_neighborhood(dataframe, "Value")

    def test_visualize_neighborhood(self):
        """
        Passing correct data frame to visualize_neighborhood
        returns map.
        """
        test_data = {"object_id": [1], "Value":[2]}
        dataframe = pd.DataFrame(data=test_data)
        test_map = visualize_neighborhood(dataframe, "Value")
        self.assertTrue(isinstance(test_map, folium.folium.Map))

    def test_missing_object_id_count(self):
        """
        Passing a data frame without object id should raise error
        in visualize_neighborhood_count
        """
        test_data = {"notObjectID": [1], "Value":[2]}
        dataframe = pd.DataFrame(data=test_data)
        with self.assertRaises(ValueError):
            visualize_neighborhood_count(dataframe)

    def test_visualize_count(self):
        """
        Passing correct data frame to visualize_neighborhood_count
        returns map.
        """
        test_data = {"object_id": [1], "Value":[2]}
        dataframe = pd.DataFrame(data=test_data)
        test_map = visualize_neighborhood_count(dataframe)
        self.assertTrue(isinstance(test_map, folium.folium.Map))

    def test_missing_object_id_mean(self):
        """
        Passing a data frame without object id should raise error
        in visualize_neighborhood_mean
        """
        test_data = {"notObjectID": [1], "Value":[2]}
        dataframe = pd.DataFrame(data=test_data)
        with self.assertRaises(ValueError):
            visualize_neighborhood_mean(dataframe, "Value")

    def test_missing_value_mean(self):
        """
        Passing a data frame without the passed value
        should raise error in visualize_neighborhood_mean
        """
        test_data = {"object_id": [1], "notValue":[2]}
        dataframe = pd.DataFrame(data=test_data)
        with self.assertRaises(ValueError):
            visualize_neighborhood_mean(dataframe, "Value")

    def test_visualize_mean(self):
        """
        Passing correct data frame to visualize_neighborhood_mean
        returns map.
        """
        test_data = {"object_id": [1], "Value":[2]}
        dataframe = pd.DataFrame(data=test_data)
        test_map = visualize_neighborhood_mean(dataframe, "Value")
        self.assertTrue(isinstance(test_map, folium.folium.Map))

    def test_visualize_heatmap_time_day(self):
        """
        Passing correct data to visualize_heatmap_with_time returns
        a map
        """
        test_data = integrate_data(COLLISIONS_DATA, 2014, WEATHER_DATA, GEO_PATH)
        test_map = visualize_heatmap_by_day(test_data, '2018-01-01', '2018-02-01')
        self.assertTrue(isinstance(test_map, folium.folium.Map))

    def test_visualize_heatmap_time_hour(self):
        """
        Passing correct data to visualize_heatmap_with_time returns
        a map
        """
        test_data = integrate_data(COLLISIONS_DATA, 2014, WEATHER_DATA, GEO_PATH)
        test_map = visualize_heatmap_by_hour(test_data, \
                   ['DOWNTOWN', 'CAPITOL HILL'], '2018-01-01', '2018-02-01')
        self.assertTrue(isinstance(test_map, folium.folium.Map))

    def test_generate_factor_list(self):
        """
        TO-DO: add docstring
        """
        test_data = integrate_data(COLLISIONS_DATA, 2014, WEATHER_DATA, GEO_PATH)
        test_dict = generate_factor_list(['weather', 'roadcond', 'collisiontype'], test_data)
        self.assertIsInstance(test_dict, dict)

    def test_roadcond_selection_widget(self):
        """
        TO-DO: add docstring
        """
        roadcond_list = ['wet', 'oil']
        test_widget = roadcond_selection_widget(roadcond_list)
        self.assertIsInstance(test_widget, widgets.widgets.widget_selection.Dropdown)

    def test_weather_selection_widget(self):
        """
        TO-DO: add docstring
        """
        weather_list = ['raining', 'snowing']
        test_widget = weather_selection_widget(weather_list)
        self.assertIsInstance(test_widget, widgets.widgets.widget_selection.Dropdown)

    def test_district_selection_widget(self):
        """
        TO-DO: add docstring
        """
        district_list = ['DOWNTOWN', 'UNIVERSITY DISTRICT']
        test_widget = district_selection_widget(district_list)
        self.assertIsInstance(test_widget, widgets.widgets.widget_selection.Dropdown)

    def test_map_by_roadcond_weather(self):
        """
        TO-DO: add docstring
        """
        test_data = integrate_data(COLLISIONS_DATA, 2014, WEATHER_DATA, GEO_PATH)
        test_map = map_by_roadcond_weather(test_data, GEO_PATH, roadcond='Wet', weather='Raining')
        self.assertIsInstance(test_map, folium.folium.Map)

    def test_map_by_roadcond(self):
        """
        TO-DO: add docstring
        """
        test_data = integrate_data(COLLISIONS_DATA, 2014, WEATHER_DATA, GEO_PATH)
        test_map = map_by_roadcond(test_data, GEO_PATH, roadcond='Dry')
        self.assertIsInstance(test_map, folium.folium.Map)

if __name__ == '__main__':
    unittest.main()
