Example Usage
=============

Overview
--------
Generally just point the method you'd like to use to the excel file output by the MultiTrace software and apply a sub-method


Noise Esimation (Absolute median deviation from signal):
--------------------------------------------------------

.. code-block:: python

    from chronoamperometry import statistics

    # Point to location of Multi-Trace data
    data = '<path to dataset>'

    # Calculate the noise in the system
    noise = statistics.Replicate_Statistics(data).calculate_median_absolute_deviation_from_signal()

    print (noise)


T-test on two independent measurements:
---------------------------------------

.. code-block:: python

    from chronoamperometry import statistics

    # importing datasets
    data1 = '<path to data for first variable>'
    data2 = '<path to data for second variable>'

    # loading data into t-test
    t_test = statistics.Experimental_Statistics(data1, data2).t_test()

    print(t_test)


Plot P-values vs time:
----------------------
.. code-block:: python

    from chronoamperometry import plotting

    # import data
    data1 = '<path to data for first variable>'
    data2 = '<path to data for second variable>'

    # plot data
    plot = plotting.ExperimentPlot(data1, data2).plot_t_test()


