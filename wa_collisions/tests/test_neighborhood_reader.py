"""
Unittests for neighborhood_reader.py
"""

import unittest
import pandas as pd
from wa_collisions.neighborhood_reader import assign_neighborhood
from wa_collisions.neighborhood_reader import get_neighborhood

# Define a class in which the tests will run
class NeighborhoodReaderTest(unittest.TestCase):
    """
    Unittests for neighborhood_reader
    """

    def test_wrong_area(self):
        """
        Tests that wrong location returns -1
        """
        object_id = get_neighborhood(0, 0)
        self.assertTrue(object_id == -1)

    def test_right_neighborhood(self):
        """
        Tests that right location return 100
        """
        # Location in Broadway neighborhood
        object_id = get_neighborhood(-122.3230027, 47.6199206)
        self.assertTrue(object_id == 100)

    def test_wrong_latitude(self):
        """
        Tests that passing non float latitude raises a value error
        """
        # Passing non float values
        with self.assertRaises(ValueError):
            get_neighborhood("a", 47.6199206)

    def test_wrong_longitude(self):
        """
        Tests that passing non float values raises a value error
        """
        # Passing non float values
        with self.assertRaises(ValueError):
            get_neighborhood(-122.3230027, "a")

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
        self.assertTrue(neighborhoods.columns.size == 3)
        self.assertTrue("X" in neighborhoods.columns)
        self.assertTrue("Y" in neighborhoods.columns)
        self.assertTrue("object_id" in neighborhoods.columns)
        self.assertTrue(neighborhoods["object_id"][0] == -1)
        self.assertTrue(neighborhoods["object_id"][1] == 100)

if __name__ == '__main__':
    unittest.main()
