"""
Unittests for render_stats.py
"""

import unittest
import pandas as pd

import wa_collisions.neighborhood_reader as neighborhood_reader
import wa_collisions.render_stats as render_stats
import wa_collisions.read_clean_integrate_data as read_clean_integrate_data

FILE_PATH = 'wa_collisions/data/Collisions_test.csv'
FILE_PATH_NBRHD = 'wa_collisions/data/Collisions_With_Neighborhoods_test.csv'

DF_NO_NEIGHBORHOODS = read_clean_integrate_data.read_collision_data(FILE_PATH)
DF_NEIGHBORHOODS = read_clean_integrate_data.read_collision_data(FILE_PATH_NBRHD)
DF_NO_NEIGHBORHOODS = read_clean_integrate_data.clean_collision_data(DF_NO_NEIGHBORHOODS)
DF_NEIGHBORHOODS = read_clean_integrate_data.clean_collision_data(DF_NEIGHBORHOODS)

# Define a class in which the tests will run
class RenderStatsTest(unittest.TestCase):
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
            render_stats.read_collision_with_neighborhoods(FILE_PATH,
                contains_neighborhood=True)

    def test_read_collision_with_neighborhoods_returns_object_id(self):
        """
        Tests that this function returns a dataframe with a field
            called 'object_id' and has at least 10 rows.
        """
        df = render_stats.read_collision_with_neighborhoods(
            FILE_PATH_NBRHD,contains_neighborhood=True)
        
        self.assertTrue('object_id' in df.columns)
        self.assertTrue(df.shape[0] > 10)

    def test_pivot_by_treatment_value_errors(self):
        #Test dataframe without neighborhood
        with self.assertRaises(ValueError):
            render_stats.pivot_by_treatment(DF_NO_NEIGHBORHOODS,treatment_list=['Genesee'])

        #Test bad path
        with self.assertRaises(ValueError):
            render_stats.pivot_by_treatment(DF_NEIGHBORHOODS,treatment_list=['Genesee'],
                neighborhood_path='bad_path')

        #Test invalid resample_by
        with self.assertRaises(ValueError):
            render_stats.pivot_by_treatment(DF_NEIGHBORHOODS,treatment_list=['Genesee']
                ,resample_by='Y')

        #Test agg_by not a string
        with self.assertRaises(ValueError):
            render_stats.pivot_by_treatment(DF_NEIGHBORHOODS,treatment_list=['Genesee']
                ,agg_by=12)
        
        #Test agg_by not a column
        with self.assertRaises(ValueError):
            render_stats.pivot_by_treatment(DF_NEIGHBORHOODS,treatment_list=['Genesee']
                ,agg_by='fake_column')

    def test_pivot_by_treatment_expected_ids_treatment(self):    
        test_treatment_in = ['Atlantic','Pike-Market', 'Belltown', 'International District',
        'Central Business District', 'First Hill', 'Yesler Terrace',
        'Pioneer Square', 'Interbay','Mann','Minor']
        
        out = render_stats.pivot_by_treatment(DF_NEIGHBORHOODS,treatment_list=test_treatment_in
            ,resample_by='D')
        
        change_speed_limit_object_count = int(len(test_treatment_in))
        same_speed_limit_object_count = int(80)

        self.assertTrue(int(out.sum()['SpeedLimitChange']) == change_speed_limit_object_count)
        self.assertTrue(int(out.sum()['SpeedLimitSame']) == same_speed_limit_object_count)

    def test_pivot_by_treatment_expected_ids_control(self):    
        test_treatment_in = ['Atlantic','Pike-Market', 'Belltown', 'International District',
        'Central Business District', 'First Hill', 'Yesler Terrace']
        test_control_in = ['Pioneer Square', 'Interbay','Mann','Minor']
        
        out = render_stats.pivot_by_treatment(DF_NEIGHBORHOODS,treatment_list=test_treatment_in
            ,control_list=test_control_in,resample_by='D')
        
        change_speed_limit_object_count = int(len(test_treatment_in))
        same_speed_limit_object_count = int(len(test_control_in))
        
        self.assertTrue(int(out.sum()['SpeedLimitChange']) == change_speed_limit_object_count)
        self.assertTrue(int(out.sum()['SpeedLimitSame']) == same_speed_limit_object_count)
    
    def test_pivot_by_treatment_resample_month(self): 
        test_treatment_in = ['Atlantic','Pike-Market', 'Belltown', 'International District',
        'Central Business District', 'First Hill', 'Yesler Terrace',
        'Pioneer Square', 'Interbay','Mann','Minor']
        
        out = render_stats.pivot_by_treatment(DF_NEIGHBORHOODS,treatment_list=test_treatment_in
            ,resample_by='M')
        
        self.assertTrue(out.index.min().month == 3)
        self.assertTrue(out.index.min().day == 31)

if __name__ == '__main__':    
    unittest.main()
