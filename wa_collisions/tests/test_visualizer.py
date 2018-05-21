"""
Unittests for visualizer.py
"""

import unittest
import pandas as pd
from wa_collisions.visualizer import visualize_neighborhood

# Define a class in which the tests will run
class VisualizerTest(unittest.TestCase):
    """
    Unittests for visualizer
    """

    def missing_column_object_id(self):
        """
        Passing a data frame without object id should raise error
        """
        test_data = {"notObjectID": [1], "Value":[2]}
        dataframe = pd.DataFrame(data=test_data)
        with self.assertRaises(ValueError):
            visualize_neighborhood(dataframe, "Value")
            
    def missing_column_mapping_value(self):
        """
        Passing a data frame without the passed mapping_value
        should raise error
        """
        test_data = {"object_id": [1], "notValue":[2]}
        dataframe = pd.DataFrame(data=test_data)
        with self.assertRaises(ValueError):
            visualize_neighborhood(dataframe, "Value")

if __name__ == '__main__':
    unittest.main()
