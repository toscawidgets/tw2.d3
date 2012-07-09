""" Samples of how to use tw2.d3

Each class exposed in the widgets submodule has an accompanying Demo<class>
widget here with some parameters filled out.

The demos implemented here are what is displayed in the tw2.devtools
WidgetBrowser.
"""

import tw2.core as twc

from widgets import (
    BarChart,
    TimeSeriesChart,
    ChordDiagram,
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

    # Top, Right, Bottom, Left
    padding = [30, 10, 10, 90]

    # The redraw interval (in milliseconds).
    interval = 1000

    data = collections.OrderedDict(
        oranges=42,
        kiwis=102,
        grapefruits=54,
        apples=21,
        bananas=63,
    )

    # This only gets called just before the widget is displayed
    def prepare(self):
        super(DemoBarChart, self).prepare()
        # Register a javascript call to a utility function that tw2.d3 provides
        # This one indicates that every element in the data should decay by a
        # certain halflife (2000ms), that function should be run every 1000ms,
        # and elements should just be removed if their value goes below a
        # certain epsilon (0.001)
        self.add_call(twc.js_function('tw2.d3.bar.schedule_halflife')(
            self.attrs['id'],
            2000,
            1000,
            0.001,
        ))
        # This registers another javascript callback that is just nice for
        # testing.  It schedules a callback that runs every 100 milliseconds
        # which adds random noise to the data elements.
        self.add_call(twc.js_function('tw2.d3.util.schedule_bump_random')(
            self.attrs['id'],
            100
        ))


class DemoTimeSeriesChart(TimeSeriesChart):
    width = 570
    n = 200
    data = [random.random() for i in range(n)]


class DemoChordDiagram(ChordDiagram):
    data = [
        [11975, 5871, 8916, 2868],
        [1951, 10048, 2060, 6171],
        [8010, 16145, 8090, 8045],
        [1013, 990, 940, 6907],
    ]
    colors = ["#000000", "#FFDD89", "#957244", "#F26223"]
