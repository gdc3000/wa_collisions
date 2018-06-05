"""
Unittests for render_stats.py
"""
import datetime
import unittest
import numpy as np
import pandas as pd
from causalimpact import CausalImpact

import wa_collisions.render_stats as render_stats
import wa_collisions.read_clean_integrate_data as read_clean_integrate_data

FILE_PATH = 'wa_collisions/data/Collisions_test.csv'
FILE_PATH_NBRHD = 'wa_collisions/data/Collisions_With_Neighborhoods_test.csv'
GEO_PATH = "wa_collisions/data/Neighborhoods/Neighborhoods.json"

#Read and clean collision data used across numerous test cases.
DF_NO_NEIGHBORHOODS = read_clean_integrate_data.read_collision_data(FILE_PATH)
DF_NEIGHBORHOODS = read_clean_integrate_data.read_collision_data(FILE_PATH_NBRHD)
DF_NO_NEIGHBORHOODS = read_clean_integrate_data.clean_collision_data(DF_NO_NEIGHBORHOODS)
DF_NEIGHBORHOODS = read_clean_integrate_data.clean_collision_data(DF_NEIGHBORHOODS)

# Define a class in which the tests will run
class RenderStatsTest(unittest.TestCase):
    """
    Unittests for render_stats
    """

    def test_bad_path(self):
        """
        Tests what happens if we pass a bad path name to
            read_collision_with_neighborhoods.
        """
        with self.assertRaises(ValueError):
            render_stats.read_collision_with_neighborhoods('fakepath')

    def test_no_object_id(self):
        """
        Tests scenario where dataframe created from filepath in
            read_collision_with_neighborhoods actually does not contain
            a neighborhood id.
        """
        with self.assertRaises(ValueError):
            render_stats.read_collision_with_neighborhoods(FILE_PATH,
                                                           contains_neighborhood=True)

    def test_returns_neighbhorhood_true_no_error(self):
        """
        Tests that read_collision_with_neighborhoods returns a dataframe with a field
            called 'object_id' and has at least 10 rows when contains_neighborhood=True.
        """
        frame = render_stats.read_collision_with_neighborhoods(
            FILE_PATH_NBRHD, contains_neighborhood=True)

        self.assertTrue('object_id' in frame.columns)
        self.assertTrue(frame.shape[0] > 10)

    def test_returns_neighbhorhood_false_no_error(self):
        """
        Tests that read_collision_with_neighborhoods returns a dataframe with a field
            called 'object_id' and has at least 10 rows when contains_neighborhood=False.
        """
        frame = render_stats.read_collision_with_neighborhoods(
            FILE_PATH, contains_neighborhood=False)

        self.assertTrue('object_id' in frame.columns)
        self.assertTrue(frame.shape[0] > 10)

    def test_geo_path_root_value_error(self):
        """
        Tests that read_collision_with_neighborhoods returns a value error if
            geo_path_root arg is not of type string.
        """
        with self.assertRaises(ValueError):
            render_stats.read_collision_with_neighborhoods(
                FILE_PATH, contains_neighborhood=False, geo_path_root=1)

        with self.assertRaises(ValueError):
            render_stats.read_collision_with_neighborhoods(
                FILE_PATH, contains_neighborhood=False, geo_path_root=None)

    def test_value_errors(self):
        """
        Tests ValueError scenarios in pivot_by_treatment_value.

        These include:
            1) trying to pivot on a dataframe with no neighborhood object_id
            2) passing a bad path for the neighborhood json file
            3) attempting to resample the data by year
            4) trying to sum by a non-string column
            5) trying to sum by a column which doesn't exist
        """
        #Test dataframe without neighborhood
        with self.assertRaises(ValueError):
            render_stats.pivot_by_treatment(DF_NO_NEIGHBORHOODS, treatment_list=['Genesee'])

        #Test bad path
        with self.assertRaises(ValueError):
            render_stats.pivot_by_treatment(DF_NEIGHBORHOODS, treatment_list=['Genesee']
                                            , neighborhood_path='bad_path')

        #Test invalid resample_by
        with self.assertRaises(ValueError):
            render_stats.pivot_by_treatment(DF_NEIGHBORHOODS, treatment_list=['Genesee']
                                            , resample_by='Y')

        #Test agg_by not a string
        with self.assertRaises(ValueError):
            render_stats.pivot_by_treatment(DF_NEIGHBORHOODS, treatment_list=['Genesee']
                                            , agg_by=12)

        #Test agg_by not a column
        with self.assertRaises(ValueError):
            render_stats.pivot_by_treatment(DF_NEIGHBORHOODS, treatment_list=['Genesee']
                                            , agg_by='fake_column')

    def test_treatment(self):
        """
        Tests that the correct number of treatment and control values are returned
            from pivot_by_treatment given a list of treatment neighborhoods.
        """

        test_treatment_in = ['Atlantic', 'Pike-Market', 'Belltown', 'International District'
                             , 'Central Business District', 'First Hill', 'Yesler Terrace'
                             , 'Pioneer Square', 'Interbay', 'Mann', 'Minor']

        out = render_stats.pivot_by_treatment(DF_NEIGHBORHOODS, treatment_list=test_treatment_in
                                              , resample_by='D')

        change_speed_limit_object_count = int(len(test_treatment_in))
        same_speed_limit_object_count = int(80)

        self.assertTrue(int(out.sum()['SpeedLimitChange']) == change_speed_limit_object_count)
        self.assertTrue(int(out.sum()['SpeedLimitSame']) == same_speed_limit_object_count)

    def test_treatment_control(self):
        """
        Tests that the correct number of treatment and control values are returned from
            pivot_by_treatment given a list of treatment neighborhoods and a list of
            control neighborhoods.
        """

        test_treatment_in = ['Atlantic', 'Pike-Market', 'Belltown', 'International District'
                             , 'Central Business District', 'First Hill', 'Yesler Terrace']
        test_control_in = ['Pioneer Square', 'Interbay', 'Mann', 'Minor']

        out = render_stats.pivot_by_treatment(DF_NEIGHBORHOODS, treatment_list=test_treatment_in
                                              , control_list=test_control_in, resample_by='D')

        change_speed_limit_object_count = int(len(test_treatment_in))
        same_speed_limit_object_count = int(len(test_control_in))

        self.assertTrue(int(out.sum()['SpeedLimitChange']) == change_speed_limit_object_count)
        self.assertTrue(int(out.sum()['SpeedLimitSame']) == same_speed_limit_object_count)

    def test_resample_month(self):
        """
        Tests the pivot_by_treatment functionality to resample the data by month, instead of day.
        """

        test_treatment_in = ['Atlantic', 'Pike-Market', 'Belltown', 'International District'
                             , 'Central Business District', 'First Hill', 'Yesler Terrace'
                             , 'Pioneer Square', 'Interbay', 'Mann', 'Minor']

        out = render_stats.pivot_by_treatment(DF_NEIGHBORHOODS, treatment_list=test_treatment_in
                                              , resample_by='M')

        self.assertTrue(out.index.min().month == 3)
        self.assertTrue(out.index.min().day == 31)

    def test_agg_by(self):
        """
        Tests the pivot_by_treatment functionality to resample the data by month, instead of day.
        """
        test_treatment_in = ['Atlantic', 'Pike-Market', 'Belltown', 'International District'
                             , 'Central Business District', 'First Hill', 'Yesler Terrace'
                             , 'Pioneer Square', 'Interbay', 'Mann', 'Minor']

        out = render_stats.pivot_by_treatment(DF_NEIGHBORHOODS, treatment_list=test_treatment_in
                                              , resample_by='D', agg_by='injuries')

        injury_count = int(out.sum()['SpeedLimitSame'])
        self.assertTrue(injury_count == 21)

    def test_transition_date_before_start(self):
        """
        Tests that a ValueError is returned when transition_date before falls before any date in the
            data.
        """
        test_treatment_in = ['Atlantic', 'Pike-Market', 'Belltown', 'International District'
                             , 'Central Business District', 'First Hill', 'Yesler Terrace'
                             , 'Pioneer Square', 'Interbay', 'Mann', 'Minor']
        transition_date = "1900-01-01"
        out_df = render_stats.pivot_by_treatment(DF_NEIGHBORHOODS, treatment_list=test_treatment_in
                                                 , resample_by='D', agg_by='injuries')
        with self.assertRaises(ValueError):
            render_stats.find_period_ranges(out_df, transition_date=transition_date)

    def test_by_day(self):
        """
        Tests the find_period_ranges function when the data is resampled by day.
        """
        test_treatment_in = ['Atlantic', 'Pike-Market', 'Belltown', 'International District'
                             , 'Central Business District', 'First Hill', 'Yesler Terrace'
                             , 'Pioneer Square', 'Interbay', 'Mann', 'Minor']
        transition_date = "2016-10-03"
        out_df = render_stats.pivot_by_treatment(DF_NEIGHBORHOODS, treatment_list=test_treatment_in
                                                 , resample_by='D', agg_by='injuries')
        out = render_stats.find_period_ranges(out_df, transition_date=transition_date)

        #Test min date
        min_date = out_df.index.min()
        min_date = datetime.date(min_date.year, min_date.month, min_date.day)
        self.assertTrue(min_date.strftime('%Y-%m-%d') == out[0][0])

        #Test transition date
        pre_transition_date = "2016-10-02"
        self.assertTrue(out[0][1] == pre_transition_date)

        #Test pre-transition date
        self.assertTrue(out[1][0] == transition_date)

        #Test max date
        max_date = out_df.index.max()
        max_date = datetime.date(max_date.year, max_date.month, max_date.day)
        self.assertTrue(max_date.strftime('%Y-%m-%d') == out[1][1])

    def test_by_month(self):
        """
        Tests the find_period_ranges function when the data is resampled by month.
        """

        test_treatment_in = ['Atlantic', 'Pike-Market', 'Belltown', 'International District'
                             , 'Central Business District', 'First Hill', 'Yesler Terrace'
                             , 'Pioneer Square', 'Interbay', 'Mann', 'Minor']
        transition_date = "2016-10-02"
        out_df = render_stats.pivot_by_treatment(DF_NEIGHBORHOODS, treatment_list=test_treatment_in
                                                 , resample_by='M', agg_by='injuries')
        out = render_stats.find_period_ranges(out_df, transition_date=transition_date)

        #Test min date
        min_date = out_df.index.min()
        min_date = datetime.date(min_date.year, min_date.month, min_date.day)
        self.assertTrue(min_date.strftime('%Y-%m-%d') == out[0][0])

        #Test transition date
        rounded_transition_date = "2016-10-31"
        self.assertTrue(rounded_transition_date == out[1][0])

        #Test max date
        max_date = out_df.index.max()
        max_date = datetime.date(max_date.year, max_date.month, max_date.day)
        self.assertTrue(max_date.strftime('%Y-%m-%d') == out[1][1])

    def test_causal_impact_load(self):
        """
        Performs a smoke test where we load causal impact.
        """
        #Setup
        test_treatment_in = ['Atlantic', 'Pike-Market', 'Belltown', 'International District'
                             , 'Central Business District', 'First Hill', 'Yesler Terrace'
                             , 'Pioneer Square', 'Interbay', 'Mann', 'Minor']
        transition_date = "2016-12-22"
        out_df = render_stats.pivot_by_treatment(DF_NEIGHBORHOODS, treatment_list=test_treatment_in
                                                 , resample_by='D', agg_by=None)
        out_date = render_stats.find_period_ranges(out_df, transition_date=transition_date)

        #Call causal impact package
        causal_impact_out = CausalImpact(out_df, out_date[0], out_date[1])

        self.assertTrue(isinstance(causal_impact_out, CausalImpact))

    def test_causal_impact_run(self):
        """
        Performs a smoke test where we run causal impact on test data. This
            test will validate Jupyter notebook dependencies.
        """
        try:
            df = pd.date_range(start='1/1/2017', end='1/08/2018')
            df = df.to_frame()
            df['SpeedLimitChange'] = np.random.normal(5, 1)
            df['SpeedLimitSame'] = np.random.normal(10, 2)
            df = df.drop([0], axis=1)

            impact_test = CausalImpact(df, ['2017-01-01', '2017-06-01']
                                       , ['2017-06-02', '2018-01-08'])
            impact_test.run()
        except KeyError:
            self.fail("test_causal_impact_run raised a KeyError.")

if __name__ == '__main__':
    unittest.main()
