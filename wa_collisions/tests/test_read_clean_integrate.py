"""
Creating Unit Tests for the module that Reads, Cleans,
and Integrates the data.
"""

import unittest

#import read_clean_integrate_data
from wa_collisions import read_clean_integrate_data

# adapted from class 3 lecture - structure of unit tests
# adapted from my homeowork 2 - the tests completed

# store the relative path to the Collisions data, Weather data and GeoJson neighborhoods data
COLLISIONS_DATA = "wa_collisions/data/Collisions_test.csv"
WEATHER_DATA = "wa_collisions/data/Weather_test.csv"
GEO_PATH = "wa_collisions/data/Neighborhoods/Neighborhoods.json"

# Define a class in which the tests will run
class IntegrateDataTest(unittest.TestCase):

    """
    Class to run Unittests.

    Class takes the unnittest.TestCase as an arguement. The class
    is designed to run through defined unit tests.
    """

    def test_smoke(self):
        """
        Test the methods in read_create_integrate_data work.

        Simple test to confirm that the method runs.
        """
        data_file = COLLISIONS_DATA
        test_data = read_clean_integrate_data.read_collision_data(data_file)
        #read_clean_integrate_data.read_weather_data("Test.csv")
        read_clean_integrate_data.clean_collision_data(test_data)
        self.assertTrue(len(test_data) > 1)


    # test the type of error that is created when the path is incorrect
    def test_file_collision(self):
        """
        Test the exception raised by the modules to read in data.

        Test the exception that is returned when an invalid path is
        supplied to read_collision_data. The incorrect path supplied
        is "test."
        """
        with self.assertRaises(ValueError):
            # supply an invalid path
            read_clean_integrate_data.read_collision_data("test")


    # test the type of error that is created when the path is incorrect
    def test_file_weather(self):
        """
        Test the exception raised by the modules to read in data.

        Test the exception that is returned when an invalid path is
        supplied to read_weather_data. The incorrect path supplied
        is "test."
        """
        with self.assertRaises(ValueError):
            # supply an invalid path
            read_clean_integrate_data.read_weather_data("test")

    def test_clean_data_collisions(self):
        """
        Test the type of data from cleaning the data.

        The data type of the date and datetime should change when the
        data are cleaned. This test confirms that there is a change.
        """
        data_file = COLLISIONS_DATA
        test_data = read_clean_integrate_data.read_collision_data(data_file)
        clean_data = read_clean_integrate_data.clean_collision_data(
            test_data,
            include_since_year=2014)
        self.assertTrue(clean_data.shape[0] > 0)

    def test_clean_data_weather(self):
        """
        Test the type of data from cleaning the data.

        The data type of the date and datetime should change when the
        data are cleaned. This test confirms that there is a change.
        """
        data_file = WEATHER_DATA
        test_data = read_clean_integrate_data.read_weather_data(data_file)
        clean_data = read_clean_integrate_data.clean_weather_data(test_data)
        self.assertTrue(
            clean_data.groupby(['year', 'month', 'day']).count().shape[0] == clean_data.shape[0])

    def test_clean_data_collisions_end_year(self):
        """
        Test the type of data from cleaning the data.

        The data type of the date and datetime should change when the
        data are cleaned. This test confirms that there is a change.
        """
        data_file = COLLISIONS_DATA
        test_data = read_clean_integrate_data.read_collision_data(data_file)
        clean_data = read_clean_integrate_data.clean_collision_data(
            test_data,
            include_since_year=2014)

        print('clean data min year:', clean_data.year.min())
        self.assertTrue(clean_data.year.min() == 2014)

        with self.assertRaises(ValueError):
            clean_data = read_clean_integrate_data.clean_collision_data(
                test_data, include_since_year='randomstring')

    def test_integrate_data(self):
        """
        Test the methods in read_create_integrate_data work.

        Simple test to confirm that the method
        integrate_data runs.
        """
        clean_data = read_clean_integrate_data.integrate_data(
            COLLISIONS_DATA, 2014, WEATHER_DATA, GEO_PATH)
        self.assertTrue(clean_data.shape[0] > 1)
        self.assertTrue('year' in clean_data.columns)
        self.assertTrue('wind_speed' in clean_data.columns)
        self.assertTrue('object_id' in clean_data.columns)
        self.assertTrue('ind_person' in clean_data.columns)

        # test if a value error is raised when passing an invalid path for collision data 
        with self.assertRaises(ValueError):
            clean_data = read_clean_integrate_data.integrate_data(
                '', 2014, WEATHER_DATA, GEO_PATH)

        # test if a value error is raised when passing an invalid path for weather data 
        with self.assertRaises(ValueError):
            clean_data = read_clean_integrate_data.integrate_data(
                COLLISIONS_DATA, 2014, '', GEO_PATH)

        # test if a value error is raised when passing an invalid path for geo_json data 
        with self.assertRaises(ValueError):
            clean_data = read_clean_integrate_data.integrate_data(
                COLLISIONS_DATA, 2014, WEATHER_DATA, '')

if __name__ == '__main__':
    unittest.main()
