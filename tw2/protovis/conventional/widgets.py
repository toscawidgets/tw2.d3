"""
TODO
"""

import tw2.core as twc
import tw2.protovis.core as twp
from tw2.protovis.core import pv

class js(twc.JSSymbol):
    def __init__(self, src):
        super(js, self).__init__(src=src)

class AreaChart(twp.PVWidget):
    p_color = twc.Param('Color of the area', default='rgb(121,173,210)')

    def prepare(self):
        super(AreaChart, self).prepare()
        # Use pre-init javascript to set up sizing and scales
        self.init_js = js(
            """
            var data = %s,
                w = %i,
                h = %i,
                x = pv.Scale.linear(data, function(d) d.x).range(0, w),
                y = pv.Scale.linear(0, 4).range(0, h);
            """ % (self.p_data, self.p_width, self.p_height))

        # Set up the root panel
        self.init().width(self.p_width).height(self.p_height) \
                .bottom(self.p_bottom).top(self.p_top) \
                .left(self.p_left).right(self.p_right)

        # X-axis and ticks
        self.add(pv.Rule) \
                .data(js('x.ticks()')) \
                .visible(js('function(d) { return d }')) \
                .left(js('x')) \
                .bottom(-5) \
                .height(5) \
                .anchor("bottom").add(pv.Label) \
                .text(js('x.tickFormat'))

        # Y-axis and ticks
        self.add(pv.Rule) \
                .data(js('y.ticks(5)')) \
                .bottom(js('y')) \
                .strokeStyle(js('function(d) { return d ? "#eee" : "#000"}')) \
                .anchor("left")\
                .add(pv.Label).text(js('y.tickFormat'))

        # The area with the top line
        self.add(pv.Area) \
                .data(js('data')) \
                .bottom(1) \
                .left(js('function(d) x(d.x)')) \
                .height(js('function(d) y(d.y)')) \
                .fillStyle(self.p_color) \
                .anchor('top').add(pv.Line).lineWidth(3)

class BarChart(twp.PVWidget):
    def prepare(self):
        super(BarChart, self).prepare()
        # Sizing and scales.
        self.init_js = js(
            """
            var data = %s,
                w = %i,
                h = %i,
                x = pv.Scale.linear(0, 1,1).range(0, w),
                y = pv.Scale.ordinal(pv.range(10)).splitBanded(0, h, 4/5);
            """ % (self.p_data, self.p_width, self.p_height))

        # Set up the root panel
        self.init().width(self.p_width).height(self.p_height) \
                .bottom(self.p_bottom).top(self.p_top) \
                .left(self.p_left).right(self.p_right)

        # The bars.
        bar = self.add(pv.Bar).data(self.p_data)\
                .top(js('function() y(this.index)'))\
                .height(js('y.range().band'))\
                .left(0)\
                .width(js('x'))

        # The value label.
        bar.anchor("right").add(pv.Label)\
                .textStyle("white")\
                .text(js('function(d) d.toFixed(1)'))

        # The variable label.
        bar.anchor("left").add(pv.Label)\
            .textMargin(5)\
            .textAlign("right")\
            .text(js('function() "ABCDEFGHIJK".charAt(this.index)'))

        # X-axis ticks.
        self.add(pv.Rule)\
            .data(js('x.ticks(5)'))\
            .left(js('x'))\
            .strokeStyle(js('function(d) d ? "rgba(255,255,255,.3)" : "#000"'))\
          .add(pv.Rule)\
            .bottom(0)\
            .height(5)\
            .strokeStyle("#000")\
          .anchor("bottom").add(pv.Label)\
            .text(js('x.tickFormat'))
