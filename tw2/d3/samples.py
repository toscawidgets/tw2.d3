""" Samples of how to use tw2.d3

Each class exposed in the widgets submodule has an accompanying Demo<class>
widget here with some parameters filled out.

The demos implemented here are what is displayed in the tw2.devtools
WidgetBrowser.
"""

from widgets import (
    BarChart,
)

import random
try:
    import collections
except ImportError:
    # Must not be on python 2.7...
    import ordereddict as collections


class DemoBarChart(BarChart):
    width = 450
    height = 120

    padding = [30, 10, 10, 80]

    data = collections.OrderedDict(
        oranges=42,
        apples=21,
        bananas=63,
    )
