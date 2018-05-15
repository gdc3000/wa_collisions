"""Creating Unit Tests for the module that Reads, Cleans, and Integrates the
    data. 

   
"""

import unittest

import read_clean_integrate_data

# adapted from class 3 lecture - structure of unit tests
# adapted from my homeowork 2 - the tests completed

# Define a class in which the tests will run
class IntegrateDataTest(unittest.TestCase):

    """ Class to run Unittests.

        Class takes the unnittest.TestCase as an arguement. The class
        is designed to run through defined unit tests.
    """

    def test_smoke(self):
        """ Test the methods in read_create_integrate_data work.

            Simple test to confirm that the method runs.
        """
        data_file = "Collisions.csv"
        test_data = read_clean_integrate_data.read_collision_data(data_file)
        read_clean_integrate_data.read_weather_data("Test.csv")
        read_clean_integrate_data.clean_collision_data(test_data)


    # test the type of error that is created when the path is incorrect
    def test_file(self):
        """ Test the exception raised by the modules to read in data.

            Test the exception that is returned when an invalid path is
            supplied to read_collision_data and read_weather_data. The
            incorrect path supplied is "test."
        """
        try:
            # supply an invalid path
            read_clean_integrate_data.read_collision_data("test")
        except Exception as err:
            self.assertTrue(isinstance(err, ValueError))
        try:
            # supply an invalid path
            read_clean_integrate_data.read_weather_data("test")
        except Exception as err:
            self.assertTrue(isinstance(err, ValueError))


if __name__ == '__main__':
    unittest.main()