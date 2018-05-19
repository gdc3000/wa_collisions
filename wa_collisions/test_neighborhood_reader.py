"""
Unittests for neighborhood_reader.py
"""

import unittest
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

if __name__ == '__main__':
    unittest.main()
