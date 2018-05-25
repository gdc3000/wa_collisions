"""
Unittests for visualizer.py
"""

import unittest
import pandas as pd
import folium
from wa_collisions.visualizer import visualize_neighborhood
from wa_collisions.visualizer import visualize_neighborhood_count
from wa_collisions.visualizer import visualize_neighborhood_mean

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

if __name__ == '__main__':
    unittest.main()
