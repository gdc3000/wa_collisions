"""
Unittests for neighborhood_reader.py
"""

import unittest
import pandas as pd
from wacollisions.neighborhood_reader import assign_neighborhood
from wacollisions.neighborhood_reader import get_neighborhood
from wacollisions.neighborhood_reader import pull_neighborhoods_file
from wacollisions.neighborhood_reader import _find_neighborhood_count

# store the relative path to the GeoJson neighborhoods data
GEO_PATH = "wacollisions/data/Neighborhoods/Neighborhoods.json"

# Define a class in which the tests will run
class NeighborhoodReaderTest(unittest.TestCase):
    """
    Unittests for neighborhood_reader
    """

    def test_wrong_area(self):
        """
        Tests that wrong location returns -1
        """
        neighborhoods = pull_neighborhoods_file()
        object_id, _, _ = get_neighborhood(0, 0, neighborhoods)
        self.assertTrue(object_id == -1)

    def test_right_neighborhood(self):
        """
        Tests that right location return 100
        """
        neighborhoods = pull_neighborhoods_file()
        # Location in Broadway neighborhood
        object_id, _, _ = get_neighborhood(
            -122.3230027, 47.6199206, neighborhoods)
        self.assertTrue(object_id == 100)

    def test_wrong_latitude(self):
        """
        Tests that passing non float latitude raises a value error
        """
        neighborhoods = pull_neighborhoods_file()
        # Passing non float values
        with self.assertRaises(ValueError):
            get_neighborhood("a", 47.6199206, neighborhoods)

    def test_wrong_longitude(self):
        """
        Tests that passing non float values raises a value error
        """
        neighborhoods = pull_neighborhoods_file()
        # Passing non float values
        with self.assertRaises(ValueError):
            get_neighborhood(-122.3230027, "a", neighborhoods)

    def test_missing_column_x(self):
        """
        Tests that passing dataframe without column X raises error
        """
        test_data = {"notX": [0], "Y":[0]}
        test_df = pd.DataFrame(data=test_data)
        with self.assertRaises(ValueError):
            assign_neighborhood(test_df)

    def test_missing_column_y(self):
        """
        Tests that passing dataframe without column Y raises error
        """
        test_data = {"X": [0], "notY":[0]}
        test_df = pd.DataFrame(data=test_data)
        with self.assertRaises(ValueError):
            assign_neighborhood(test_df)

    def test_correct_data(self):
        """
        Tests that passing correct values to assign neighborhood
        returns correct neighborhood.
        """
        test_data = {"X": [0, -122.3230027], "Y":[0, 47.6199206]}
        test_df = pd.DataFrame(data=test_data)
        neighborhoods = assign_neighborhood(test_df)
        self.assertTrue(len(neighborhoods) == 2)
        self.assertTrue(neighborhoods.columns.size == 5)
        self.assertTrue("X" in neighborhoods.columns)
        self.assertTrue("Y" in neighborhoods.columns)
        self.assertTrue("object_id" in neighborhoods.columns)
        self.assertTrue(neighborhoods["object_id"][0] == -1)
        self.assertTrue(neighborhoods["object_id"][1] == 100)

    def test_find_neighborhood_count(self):
        """
        Test to see if the find_neighborhood_count function
        returns the correct number of neighborhoods.
        """
        counts = _find_neighborhood_count(None, GEO_PATH)
        self.assertTrue(counts == 119)

if __name__ == '__main__':
    unittest.main()
