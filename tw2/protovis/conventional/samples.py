""" Samples of how to use tw2.jit

Each class exposed in the widgets submodule has an accompanying Demo<class>
widget here with some parameters filled out.

The demos implemented here are what is displayed in the tw2.devtools
WidgetBrowser.
"""
from widgets import AreaChart
from tw2.core import JSSymbol

import math
import random

class DemoAreaChart(AreaChart):
    py_data = [{'x': i, 'y' : math.sin(i) + random.random() * .5 + 2}
                for i in map(lambda x : x / 10.0, range(100))]
