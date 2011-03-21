""" Samples of how to use tw2.protovis.conventional

Each class exposed in the widgets submodule has an accompanying Demo<class>
widget here with some parameters filled out.

The demos implemented here are what is displayed in the tw2.devtools
WidgetBrowser.
"""
from widgets import (
    AreaChart,
    BarChart,
    ScatterPlot,
    PieChart,
    LineChart,
    StackedAreaChart,
    GroupedBarChart
)
from widgets import js
from tw2.core import JSSymbol

import math
import random
import time

class DemoAreaChart(AreaChart):
    p_data = [{'x': i, 'y' : math.sin(i) + random.random() * .5 + 2}
                for i in map(lambda x : x / 10.0, range(100))]

class DemoBarChart(BarChart):
    p_data = [random.random()*100 for i in range(10)]
    p_labels = ['label ' + str(i) for i in range(10)]

class DemoScatterPlot(ScatterPlot):
    p_data = [{'x': i, 'y' : random.random(), 'z' : 10**(2*random.random())}
                for i in range(100)]

class DemoPieChart(PieChart):
    p_data = [random.random() for i in range(10)]


class AutoRefreshingData(object):
    """ Helper class for DemoLineChart.  Refreshes its data dynamically. """
    def __iter__(self):
        n = 20.0
        T_scale = 1000.0
        now = int(time.time())
        tspan = range(now-100, now)
        funcs = [
            lambda t : math.sin(t/n),
            lambda t : abs(math.sin(t/n))**((t%(2*n))/n),
            lambda t : math.cos(t/(n+1))*1.5,
        ]
        funcs.append(
            lambda t : funcs[1](t) * funcs[2](t)
        )

        for i in range(len(funcs)):
            yield [ { 'x': t*1000.0, 'y' : funcs[i](float(t)) } for t in tspan ]

    def __repr__(self):
        print "repr"
        return str(self)

    def __str__(self):
        return str([ele for ele in self])

    def __len__(self):
        return 4

class DemoLineChart(LineChart):
    p_data = AutoRefreshingData()
    p_labels = ["billy", "bobby", "sally", "suzie"]
    p_time_series = True

class DemoStackedAreaChart(StackedAreaChart):
    p_data = [
        [
            {
                'series' : i,
                'x': j / 10.0,
                'y' : math.sin(j/10.0) + random.random() * .5  + 2
            } for j in range(100)
        ] for i in range(5)
    ]
    p_labels = ["billy", "bobby", "sally", "suzie", "balthazar"]

class DemoGroupedBarChart(GroupedBarChart):
    p_data = [
        [random.random() + 0.1 for j in range(4)] for i in range(3)]
    p_labels = ['DataSet1', 'Dataset2', 'Dataset3']
