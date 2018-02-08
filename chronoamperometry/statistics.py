from scipy import stats
import pandas as pd
import numpy as np
from tqdm import tqdm
from chronoamperometry import utils


class ReplicateStatistics(object):

    """ This class contains statistical tools for the analysis of replicate traces """

    def __init__(self, data, span=0.2, df_name='mads_df', periodicity=None, cycles=None, stabilization_time=None):
        if type(data) == str and data.lower().endswith('.xlsx'):
            self.dataframe = utils.DataFrameBuild(data).melted_dataframe_from_mtxl()[0]
            self.channels = utils.DataFrameBuild(data).melted_dataframe_from_mtxl()[1]
        elif data.internal_cache == 'melted':
            self.dataframe = data
            self.channels = data.Channel.unique().tolist()
        elif data.internal_cache == 'unmelted':
            ch_names = data.Channel.unique().tolist()
            df = pd.melt(data, id_vars=['Time'], value_vars=ch_names, var_name='Channel', value_name='Current')
            df.internal_cache = 'melted'
            self.dataframe = df
            self.channels = ch_names
        self.span = span
        self.df_name = df_name
        self.periodicity = periodicity
        self.stabilization = stabilization_time
        self.cycles = cycles

    def construct_lowess_regression(self):
        '''
        Creates a smoothed regression based on the Lowess algorithm.
        '''

        from statsmodels.nonparametric.smoothers_lowess import lowess

        df = self.dataframe
        channels = self.channels
        span = float(self.span)

        dfs = dict(list(df.groupby("Channel")))

        dfs_lo = []

        for i in tqdm(range(0, len(channels))):
            dfs_i = dfs[channels[i]]

            x = dfs_i['Time']
            x = np.asarray(x)

            y = dfs_i['Current']
            y = np.asarray(y)

            lo = lowess(y, x, frac=span, it=1, delta=0.0, is_sorted=True, return_sorted=False)

            dfs_lo.append(lo)

        dfs_lo = np.concatenate(dfs_lo).ravel()  # .tolist()

        # print (dfs_lo)

        # exit()

        df['Regression'] = dfs_lo

        df.internal_cache = 'regression'

        return df

    def calculate_median_absolute_deviation_from_signal(self):
        '''
        Estimates noise by calculating distance of median noise in the traces
        from the 'signals' produced by the regression analysis
        '''

        df = self.dataframe
        channels = self.channels

        if df.internal_cache == 'regression':
            pass
        elif df.internal_cache == 'melted':
            print ('median absolute deviation from signal calculation requires regression fitting first!')
            print ('running regression fitting analysis...')
            df = ReplicateStatistics(df).construct_lowess_regression()

        dfs = dict(list(df.groupby("Channel")))

        ads_list = []
        ch_list = []

        print('calculating median absolute deviation of measured current from regression signal...')

        for i in tqdm(range(0, len(channels))):
            dfs_i = dfs[channels[i]]

            n = dfs_i['Current']
            n = np.asarray(n)

            s = dfs_i['Regression']
            s = np.asarray(s)

            d = np.median(abs(np.subtract(n, s)))

            ads_list.append(d)

            ch_list.append('CH' + str(i + 1))

        ads_df = pd.DataFrame(ads_list, columns=['Deviation'])

        ads_df['Experiment'] = self.df_name
        ads_df['Channel'] = ch_list

        # ads_df['Channel']

        # print(ads_df)

        ads_df.internal_cache = 'MADS'

        return ads_df

    def calculate_absolute_deviation_from_signal_per_channel(self):
        '''
        Estimates noise by calculating distance of the noise of each trace
        from the 'signal' produced by the regression analysis
        '''

        df = self.dataframe
        channels = self.channels

        if df.internal_cache == 'regression':
            pass
        elif df.internal_cache == 'melted':
            print ('median absolute deviation from signal calculation requires regression fitting first!')
            print ('running regression fitting analysis...')
            df = ReplicateStatistics(df).construct_lowess_regression()

        dfs = dict(list(df.groupby("Channel")))

        ads_list = []

        print('calculating median absolute deviation of measured current from regression signal...')

        for i in tqdm(range(0, len(channels))):
            dfs_i = dfs[channels[i]]

            n = dfs_i['Current']
            n = np.asarray(n)

            s = dfs_i['Regression']
            s = np.asarray(s)

            d = abs(np.subtract(n, s))

            ads_list.append(d)

        dfs_ads = np.concatenate(ads_list).ravel()  # .tolist()

        df['Deviation'] = dfs_ads

        df.internal_cache = 'P/C_MADS'

        return df

    def anova_test_magnitude_of_current_variance(self):
        """

        Anova

        Not Working Yet
        :return:
        """
        if self.stabilization is None:
            print('You need to specify the stabilization time: the amount of time that passed before '
                  'initiation of periodic peturbment of fuel cell')
            exit(code=10)
        else:
            pass

        if self.periodicity is None:
            print('You need to specify the periodic cycle length.')
            exit(code=11)
        else:
            pass

        if self.cycles is None:
            print('You need to specify the number of cycles.')
            exit(code=12)
        else:
            pass

        df = self.dataframe
        channels = self.channels

        ch_list = []
        og_ch_list = []

        print('Running Analysis of Variance...')

        for i in (range(0, len(channels))):
            ch_list.append('CH' + str(i + 1))
            og_ch_list.append('CH' + str(i + 1))

        df = df.set_index('Channel')

        # currents = np.empty(1, 60001)
        currents = []

        for i in tqdm(range(0, len(ch_list))):
            single_channel_df = df.loc[ch_list[i]]
            # print(single_channel_df)
            single_channel_array = single_channel_df.as_matrix(columns=['Current'])
            # print(single_channel_array)
            single_channel_array = single_channel_array.flatten()
            # print(single_channel_array.shape)
            # np.append(currents, single_channel_array, axis=1)
            currents.append(single_channel_array.tolist())

        print(currents)

        f_val, p_val = stats.f_oneway(currents)

        print("One-way ANOVA P =", p_val)
        print('One-Way ANOVA F =', f_val)

        # print (ch_list)

        return anova


class ExperimentalStatistics(object):

    """
    This class contains tools for the analysis of a single variable between two groups of replicate traces.

    """

    def __init__(self, data1, data2, span=0.2, significance_threshold=0.05):

        self.significance = significance_threshold
        self.span = span

        if type(data1) == str and data1.lower().endswith('.xlsx'):
            self.data1 = utils.DataFrameBuild(data1).dataframe_from_mtxl()[0]
        elif data1.internal_cache == 'unmelted':
            self.data1 = data1
        elif data1.internal_cache == 'melted':
            df = data1.pivot_table(values='Current', index='Time', columns='Channel').reset_index()
            df.internal_cache = 'unmelted'
            self.data1 = df
        else:
            pass

        if type(data2) == str and data2.lower().endswith('.xlsx'):
            self.data2 = utils.DataFrameBuild(data2).dataframe_from_mtxl()[0]
        elif data2.internal_cache == 'unmelted':
            self.data2 = data2
        elif data2.internal_cache == 'melted':
            df = data2.pivot_table(values='Current', index='Time', columns='Channel').reset_index()
            df.internal_cache = 'unmelted'
            self.data2 = df
        else:
            pass

    def compare_absolute_deviation_from_signal_between_experiments(self):
        '''
        Allows for a comparison of noise between two experiments with a single variable
        '''

        span = self.span
        df1 = self.data1
        df2 = self.data2

        df1 = ReplicateStatistics(df1, span).construct_lowess_regression()
        df2 = ReplicateStatistics(df2, span).construct_lowess_regression()

        ads_df1 = ReplicateStatistics(df1).calculate_median_absolute_deviation_from_signal()
        ads_df2 = ReplicateStatistics(df2).calculate_median_absolute_deviation_from_signal()

        all_df = ads_df1.append(ads_df2)

        all_df.internal_cache = 'ads_ex'
        ads_df1.internal_cache = 'ads_ex'
        ads_df2.internal_cache = 'ads_ex'

        return ads_df1, ads_df2

    def t_test(self):
        '''
        t-test on raw chronoamperometric data
        '''

        import pandas as pd
        import numpy as np
        import scipy as sp
        import utils

        df1 = self.data1
        df2 = self.data2

        df_current1 = df1.ix[:, 1:]
        df_current2 = df2.ix[:, 1:]

        len1 = len(df_current1.index)
        len2 = len(df_current2.index)

        if len1 < len2:
            time_length = len1
            time = np.array(df1.ix[:, 0].values.tolist())
        else:
            time_length = len2
            time = np.array(df2.ix[:, 0].values.tolist())

        # mean1_list = []
        # mean2_list = []

        # standard_deviation_list1 = []
        # standard_deviation_list2 = []

        # t_stat_list = []
        # p_value_list = []

        df = pd.DataFrame(
            columns=['Time', 'Mean 1', 'Mean 2', 'Standard Deviation 1', 'Standard Deviation 2', 'T Statistic',
                     'P Value', 'Significance'])

        print(df)

        for i in tqdm(range(0, time_length)):
            point = time[i]

            currents1 = df_current1.ix[i].values.tolist()
            currents2 = df_current2.ix[i].values.tolist()

            currents1 = np.array(currents1)
            currents2 = np.array(currents2)

            mean1 = np.mean(currents1, axis=0)
            mean2 = np.mean(currents2, axis=0)

            # mean1_list.append(mean1)
            # mean2_list.append(mean2)

            std1 = np.std(currents1, axis=0)
            std2 = np.std(currents2, axis=0)
            # standard_deviation_list1.append(std1)
            # standard_deviation_list2.append(std2)

            t_stat, p_value = sp.stats.ttest_ind(currents1, currents2, equal_var=False)
            # t_stat_list.append(t_stat)
            # p_value_list.append(p_value)

            significance = self.significance

            row = [point, mean1, mean2, std1, std2, t_stat, p_value, significance]

            dfi = pd.DataFrame([[point, mean1, mean2, std1, std2, t_stat, p_value, significance]],
                               columns=['Time', 'Mean 1', 'Mean 2', 'Standard Deviation 1', 'Standard Deviation 2',
                                        'T Statistic', 'P Value', 'Significance'])

            # print(dfi)

            df = df.append(dfi, ignore_index=True)

        df.internal_cache = 't_test'

        # print(df)

        return df

    def anova_test(self):
        """
        returns an an analysis of variance comparing distribution of current magnitude between
         two experiments at each timepoint.
        """

        import pandas as pd
        import numpy as np
        import scipy as sp
        import utils

        print('Running Analysis of Variance...')

        df1 = self.data1
        df2 = self.data2

        df_current1 = df1.ix[:, 1:]
        df_current2 = df2.ix[:, 1:]

        len1 = len(df_current1.index)
        len2 = len(df_current2.index)

        if len1 < len2:
            time_length = len1
            time = np.array(df1.ix[:, 0].values.tolist())
        else:
            time_length = len2
            time = np.array(df2.ix[:, 0].values.tolist())

        # mean1_list = []
        # mean2_list = []

        # standard_deviation_list1 = []
        # standard_deviation_list2 = []

        # t_stat_list = []
        # p_value_list = []

        df = pd.DataFrame(columns=['Time', 'F-Value', 'P-Value'])

        # print(df)

        for i in tqdm(range(0, time_length)):
            point = time[i]

            currents1 = df_current1.ix[i].values.tolist()
            currents2 = df_current2.ix[i].values.tolist()

            currents1 = np.array(currents1)
            currents2 = np.array(currents2)

            f_val, p_val = stats.f_oneway(currents1, currents2)

            dfi = pd.DataFrame([[point, f_val, p_val]], columns=['Time', 'F-Value', 'P-Value'])

            # print(dfi)

            df = df.append(dfi, ignore_index=True)

        df.internal_cache = 'anova_test'

        # print(df)

        return df

