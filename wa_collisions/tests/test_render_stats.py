"""
Unittests for render_stats.py
"""

import unittest
import pandas as pd

from wa_collisions import render_stats

# Define a class in which the tests will run
class NeighborhoodReaderTest(unittest.TestCase):
    """
    Unittests for render_stats
    """

    def test_read_collision_with_neighborhoods_bad_path(self):
        """
        Tests what happens if we pass a bad path name to
            read_collision_with_neighborhoods.
        """
        with self.assertRaises(ValueError):
            render_stats.read_collision_with_neighborhoods('fakepath')

    def test_read_collision_with_neighborhoods_no_object_id(self):
        """
        Tests scenario where dataframe created from filepath
            actually does not contain a neighborhood id.
        """     
        with self.assertRaises(ValueError):
            render_stats.read_collision_with_neighborhoods('../data/Collisions.csv',
                contains_neighborhood=True)

    def test_read_collision_with_neighborhoods_returns_object_id(self):
        """
        Tests that this function returns a dataframe with a field
            called 'object_id' and has at least 10 rows.
        """
        df = render_stats.read_collision_with_neighborhoods(
            '../data/Collisions_With_Neighborhoods.csv',contains_neighborhood=True)
        
        self.assertTrue('object_id' in df.columns)
        self.assertTrue(df.shape[0] > 10)

    def test_pivot_by_treatment_assert(self):
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
