import pandas as pd
import numpy as np
from time import sleep


class DataFrameBuild(object):

    """
    This class consumes excel file outputs from PalmSens Multitrace and converts them to a standardized
    pandas dataframe format

    """

    def __init__(self, mt_excel_data):
        self.excel_data = str(mt_excel_data)

    def dataframe_from_mtxl(self):

        """
        Consumes excel files and produces unmelted dataframes where each column is a different channel, except the first,
        which is time.

        """

        df = pd.read_excel(self.excel_data, encoding='utf8', skiprows=range(1, 2))

        headers = list(df.columns.values)

        times = headers[0::2]
        bad_times = headers[2::2]
        data = headers[1::2]

        ch_names = [s.encode('ascii') for s in times]
        ch_names = [x.strip(' ') for x in ch_names]

        df = df.drop(bad_times, axis=1)

        df.columns = ['Time'] + ch_names

        df = df.astype(np.float64)
        df = df.round(decimals=4)

        df.internal_cache = 'unmelted'
        #  df.added_property = 'property'

        return df, ch_names

    def melted_dataframe_from_mtxl(self):

        """
        Consumes excel files and produces melted dataframes, grammar of graphics style.

        """

        df = pd.read_excel(self.excel_data, encoding='utf8', skiprows=range(1, 2))

        headers = list(df.columns.values)

        times = headers[0::2]
        bad_times = headers[2::2]
        data = headers[1::2]

        ch_names = [s.encode('ascii') for s in times]
        ch_names = [x.strip(' ') for x in ch_names]

        # print(ch_names)

        df = df.drop(bad_times, axis=1)

        df.columns = ['Time'] + ch_names

        df = df.astype(np.float64)
        df = df.round(decimals=4)

        df = pd.melt(df, id_vars=['Time'], value_vars=ch_names, var_name='Channel', value_name='Current')

        df.internal_cache = 'melted'

        return df, ch_names


class SelectData(object):

    """
    This class is useful for splitting data into two subsets (e.g.: if there are different variables on the
    same run, etc.) or for deleting a subset of the data. Simply pass in a list of channel numbers that should be
     in the first or second subsets.

    """

    def __init__(self, data, subset_1=None, subset_2=None):
        if subset_1 is None:
            raise Exception('Requires first data subset channels to be defined!')
        elif subset_1 is type(list) or type(int):
            self.var1chs = subset_1
        else:
            raise Exception('Requires input of channels as a list of integers')

        if subset_2 is None:
            raise Exception('Requires second data subset channels to be defined!')
        elif subset_2 is type(list) or type(int):
            self.var2chs = subset_2
        else:
            raise Exception('Requires input of channels as a list of integers')

        if type(data) is str and data.lower().endswith('.xlsx'):
            self.dataframe = DataFrameBuild(data).melted_dataframe_from_mtxl()[0]
            self.channels = DataFrameBuild(data).melted_dataframe_from_mtxl()[1]
        elif data.internal_cache == 'melted':
            self.dataframe = data
            self.channels = data.Channel.unique().tolist()
        elif data.internal_cache == 'unmelted':
            ch_names = data.Channel.unique().tolist()
            df = pd.melt(data, id_vars=['Time'], value_vars=ch_names, var_name='Channel', value_name='Current')
            df.internal_cache = 'melted'
            self.dataframe = df
            self.channels = ch_names

    def split_dataframes(self):

        """
        This method will convert the raw output from the PalmSens Multitrace software for the MultiEmStat potentiostat
        or a processed dataframe to multiple dataframes, one for each experimental variable so that they can be compared.

        Is useful for multiple variables on the same device

        """

        df = self.dataframe
        channels = self.channels
        if isinstance(self.var1chs, list):
            var1_chs = ['CH' + str(int(self.var1chs[i])) for i in range(len(self.var1chs))]
        elif isinstance(self.var1chs, int):
            var1_chs = 'CH' + str(int(self.var1chs))
        else:
            print(type(self.var1chs))

        if isinstance(self.var2chs, list):
            var2_chs = ['CH' + str(int(self.var2chs[i])) for i in range(len(self.var2chs))]
        elif isinstance(self.var2chs, int):
            var2_chs = 'CH' + str(int(self.var2chs))
        else:
            print(type(self.var2chs))

        # dfs = dict(list(df.groupby("Channel")))

        df_var1 = []
        df_var2 = []

        for o in range(len(channels)):
            ch_df_name = list(list(df.groupby("Channel"))[o])[0]
            ch_df = list(list(df.groupby("Channel"))[o])[1]

            # print(ch_df)
            print(ch_df_name)

            for i in range(len(var1_chs)):
                if str(var1_chs[i]) == str(ch_df_name):
                    df_var1.append(ch_df)
                else:
                    pass

            for i in range(len(var2_chs)):
                if str(var2_chs[i]) == str(ch_df_name):
                    df_var2.append(ch_df)
                else:
                    pass

        df_var1 = pd.concat(df_var1).reset_index(drop=True)
        df_var2 = pd.concat(df_var2).reset_index(drop=True)

        return df_var1, df_var2

    def delete_subset(self):

        """
        This method will keep the first subset and delete the second subset of the input data.

        """

        df = self.dataframe
        channels = self.channels
        if isinstance(self.var1chs, list):
            keep_chs = ['CH' + str(int(self.var1chs[i])) for i in range(len(self.var1chs))]
        elif isinstance(self.var1chs, int):
            keep_chs = 'CH' + str(int(self.var1chs))
        else:
            print(type(self.var1chs))

        df_var1 = []

        for o in range(len(channels)):
            ch_df_name = list(list(df.groupby("Channel"))[o])[0]
            ch_df = list(list(df.groupby("Channel"))[o])[1]

            # print(ch_df)
            print(ch_df_name)

            for i in range(len(keep_chs)):
                if str(keep_chs[i]) == str(ch_df_name):
                    df_var1.append(ch_df)
                else:
                    pass

        df_var1 = pd.concat(df_var1).reset_index(drop=True)

        return df_var1

