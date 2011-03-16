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

class DemoLineChart(LineChart):
    p_data = [
        [
            {
                'x': i,
                'y' : math.sin((i) + random.random()) +
                (j/12.0)*random.random() + (j/3.0) + 0.5
            } for i in map(lambda x : x / 5.0, range(50))
        ] for j in range(6)
    ]
    p_labels = ["billy", "bobby", "sally", "suzie", "balthazar", "quetzalcoatl"]
    p_interpolate = 'basis'

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
