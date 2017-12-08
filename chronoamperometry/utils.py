import pandas as pd
import numpy as np


class DataFrameBuild(object):

    def __init__(self, mt_excel_data):
        self.excel_data = str(mt_excel_data)

    def dataframe_from_mtxl(self):

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


