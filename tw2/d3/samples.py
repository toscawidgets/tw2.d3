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

class DemoBarChart(BarChart):
    data = [
        {
            'key': i,
            'value': random.random(),
        } for i in range(10)
    ]
