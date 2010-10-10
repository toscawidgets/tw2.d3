""" Samples of how to use tw2.jit

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
    StreamGraph,
)
from widgets import js
from tw2.core import JSSymbol

import math
import random

class DemoAreaChart(AreaChart):
    p_data = [{'x': i, 'y' : math.sin(i) + random.random() * .5 + 2}
                for i in map(lambda x : x / 10.0, range(100))]

class DemoBarChart(BarChart):
    p_data = [random.random() for i in range(10)]

class DemoScatterPlot(ScatterPlot):
    p_data = [{'x': i, 'y' : random.random(), 'z' : 10**(2*random.random())}
                for i in range(100)]

class DemoPieChart(PieChart):
    p_data = [random.random() for i in range(10)]

# The following are some data generation functions used by the streamgraph demo
def waves(n, m):
    def f(i, j):
        x = 20 * j / m - i / 3
        if x > 0:
            return 2 * x * math.exp(x * -0.5)
        return 0
    return map(lambda i : map(lambda j : f(i, j), range(m)), range(n))

def layers(n, m):
    def bump(a):
        x = 1.0 / (.1 + random.random())
        y = 2.0 * random.random() - 0.5
        z = 10.0 / (0.1 + random.random())
        for i in range(m):
            w = (float(i) / m - y) * z
            a[i] += x * math.exp(-w * w)
        return a
    def f(*args):
        a = [0] * m
        for i in range(5):
            a = bump(a)
        return a
    return map(f, range(n))


class DemoStreamGraph(StreamGraph):
    def prepare(self):
        self.p_data = layers(20, 400)
        super(DemoStreamGraph, self).prepare()
