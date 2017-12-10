# encoding: utf-8
import plotnine
from chronoamperometry import utils, statistics
import pandas as pd
import matplotlib
matplotlib.use('TkAgg')


class ReplicatePlot(object):
    """
    Is designed to plot replicates from a single experiment.

    """

    def __init__(self, data, span=0.2):
        if type(data) == str and data.lower().endswith('.xlsx'):
            self.data = utils.DataFrameBuild(data).melted_dataframe_from_mtxl()[0]
        elif data.internal_cache == 'melted':
            self.data = data
        elif data.internal_cache == 'unmelted':
            ch_names = data.Channel.unique().tolist()
            df = pd.melt(data, id_vars=['Time'], value_vars=ch_names, var_name='Channel', value_name='Current')
            df.internal_cache = 'melted'
            self.data = df
            self.span = span

    def plot_replicates(self):

        """
        Plots replicate traces from a single run. Color is assigned randomly.

        """

        from plotnine import ggplot, ylab, xlab, geom_line, aes, stat_smooth, geom_smooth

        plot = (

            (ggplot(self.data, aes('Time', 'Current', color='Channel'))
                + ylab(u'Current (μA)')
                + xlab('Time (seconds)')
                + geom_line())

        )

        print (plot)
        return plot

    def plot_replicates_log_axes(self):

        """
        Plots replicate traces from a single run on logarithmic axes to determine the baseline metabolic charge production
        or other stabilization.

        """

        from plotnine import ggplot, ylab, xlab, geom_line, aes, scale_y_log10, scale_x_log10

        plot = (

            (ggplot(self.data, aes('Time', 'Current', color='Channel'))
             + ylab(u'Current (μA)')
             + xlab('Time (seconds)')
             + geom_line()
             + scale_y_log10()
             + scale_x_log10())

        )

        print (plot)
        return plot

    def plot_replicates_greyscale(self):

        """
        Some journals require greyscale graphs. This method makes that simple.

        """

        from plotnine import ggplot, ylab, xlab, geom_line, aes, theme_bw, scale_color_grey

        plot = (

            (ggplot(self.data, aes('Time', 'Current', color='Channel'))
             + ylab(u'Current (μA)')
             + xlab('Time (seconds)')
             + geom_line()
             + theme_bw()
             + scale_color_grey())

        )

        print (plot)
        return plot

    def plot_replicates_lowess_regression_smoothing(self):

        """
        Applies a lowess smoothing regression to replicates plot in order to estimate the true function.

        """

        from plotnine import ggplot, ylab, xlab, geom_line, aes, geom_smooth, theme_bw, scale_color_grey

        plot = (

            (ggplot(self.data, aes('Time', 'Current', color='Channel'))
             + ylab(u'Current (μA)')
             + xlab('Time (seconds)')
             + geom_line()
             + theme_bw()
             + scale_color_grey()
             + geom_smooth(span=self.span, method='lowess'))

        )

        print (plot)
        return plot


class VariablePlot(object):
    """
    Plots the variation from the true function on a per-channel basis... will add more functions later.

    """

    def __init__(self, data):
        if type(data) == str and data.lower().endswith('.xlsx'):
            self.data = utils.DataFrameBuild(data).melted_dataframe_from_mtxl()[0]
        elif data.internal_cache == 'melted':
            self.data = data
        elif data.internal_cache == 'unmelted':
            ch_names = data.Channel.unique().tolist()
            df = pd.melt(data, id_vars=['Time'], value_vars=ch_names, var_name='Channel', value_name='Current')
            df.internal_cache = 'melted'
            self.data = df
        else:
            pass

    def plot_absolute_deviation_from_signal_per_channel(self):
        """
        Boxplots of the distance of the raw noisy data from the lowess smoothing function
        for each channel. The lowess regression is taken to be an esimation of the true function.

        """

        from plotnine import ggplot, aes, stat_boxplot

        if self.data.internal_cache == 'P/C_MADS':
            dev_df = self.data
        elif self.data.internal_cache == 'melted':
            dev_df = statistics.Replicate_Statistics(self.data).calculate_absolute_deviation_from_signal_per_channel()

        plot = (

            (ggplot(dev_df, aes('Channel', 'Deviation'))
             + stat_boxplot())

        )

        print (plot)
        return plot


class ExperimentPlot(object):
    """
    Plots comparisons between experiments.

    """

    def __init__(self, data1, data2):
        self.data1 = data1
        self.data2 = data2
        self.t_test_df = statistics.Experimental_Statistics(data1, data2).t_test()

    def plot_t_test(self):
        """
        Plots p-value vs time

        """
        from plotnine import ggplot, aes, ylab, xlab, geom_line
        df = self.t_test_df

        plot = (

            (ggplot(df, aes('Time', 'P Value'))
             + ylab('P Value')
             + xlab('Time (seconds)')
             + geom_line())

        )

        print (plot)
        return plot

    def plot_means_after_t_test(self):
        """
        Plots means of the two experiments vs time

        """
        from plotnine import ggplot, aes, ylab, xlab, geom_line
        df = self.t_test_df

        plot = (

            (ggplot(df, aes('Time', 'Mean 1'))
             + ylab(u'Average Current (μA)')
             + xlab('Time (seconds)')
             + geom_line()
             + geom_line(aes('Time', 'Mean 2')))

        )

        print (plot)
        return plot

    def plot_standard_deviation_after_t_test(self):
        """
        Plots standard deviation of two experiments vs time.

        """
        from plotnine import ggplot, aes, ylab, xlab, geom_line
        df = self.t_test_df

        plot = (

            (ggplot(df, aes('Time', 'Standard Deviation 1'))
             + ylab('Standard Deviation')
             + xlab('Time (seconds)')
             + geom_line()
             + geom_line(aes('Time', 'Standard Deviation 2')))

        )

        print (plot)
        return plot

    def plot_median_absolute_deviation_from_signal(self):
        """
        boxplot of median absolute deviation from the lowess regression for two experiments. Is an estimation of the
        difference in magnitude of noise for each experiment. Broken in last update.

        """


        from plotnine import ggplot, aes, stat_boxplot

        if self.data.internal_cache == 'MADS':
            ads = self.data
        elif self.data.internal_cache == 'melted':
            ads = statistics.Replicate_Statistics(self.data).calculate_median_absolute_deviation_from_signal()

        plot = (

            (ggplot(ads, aes('Experiment', 'Deviation'))
             + stat_boxplot())

        )

        print (plot)
        return plot

