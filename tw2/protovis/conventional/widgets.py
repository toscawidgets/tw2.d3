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

        self.setupRootPanel()

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
    p_labels = twc.Param('list of label strings')
    def prepare(self):
        if len(self.p_labels) != len(self.p_data):
           raise ValueError, 'Barchart must have same # of labels and data'

        super(BarChart, self).prepare()

        # Sizing and scales.
        self.init_js = js(
            """
            var data = %s,
                w = %i,
                h = %i,
                x = pv.Scale.linear(0, pv.max(data)).range(0, w),
                y = pv.Scale.ordinal(pv.range(data.length)).splitBanded(0, h, 4/5),
                labels = %s;
            """ % (self.p_data, self.p_width, self.p_height, self.p_labels))

        self.p_left = 9 * max([len(items) for items in self.p_labels])+2

        self.setupRootPanel()

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
            .text(js('function() labels[this.index]'))

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

class ScatterPlot(twp.PVWidget):
    def prepare(self):

        super(ScatterPlot, self).prepare()

        # Sizing and scales.
        self.init_js = js(
            """
            var data = %s,
                w = %i,
                h = %i,
                x = pv.Scale.linear(0, 99).range(0, w),
                y = pv.Scale.linear(0, 1).range(0, h),
                c = pv.Scale.log(1, 100).range("orange", "brown");
            """ % (self.p_data, self.p_width, self.p_height))

        self.setupRootPanel()

        # Y-axis and ticks.
        self.add(pv.Rule) \
            .data(js('y.ticks()')) \
            .bottom(js('y')) \
            .strokeStyle(js('function(d) d ? "#eee" : "#000"')) \
          .anchor("left").add(pv.Label) \
            .visible(js('function(d) d > 0 && d < 1')) \
            .text(js('y.tickFormat'))

        # X-axis and ticks.
        self.add(pv.Rule) \
            .data(js('x.ticks()')) \
            .left(js('x')) \
            .strokeStyle(js('function(d) d ? "#eee" : "#000"')) \
          .anchor("bottom").add(pv.Label) \
            .visible(js('function(d) d > 0 && d < 100')) \
            .text(js('x.tickFormat'))

        # The dot plot!
        self.add(pv.Panel) \
            .data(js('data')) \
          .add(pv.Dot) \
            .left(js('function(d) x(d.x)')) \
            .bottom(js('function(d) y(d.y)')) \
            .strokeStyle(js('function(d) c(d.z)'))  \
            .fillStyle(js('function() this.strokeStyle().alpha(.2)'))  \
            .size(js('function(d) d.z')) \
            .title(js('function(d) d.z.toFixed(1)'))

class PieChart(twp.PVWidget):
    def prepare(self):

        super(PieChart, self).prepare()

        # Sizing and scales.
        self.init_js = js(
            """
            var data = %s,
                w = %i,
                h = %i,
                r = h > w ? w / 2 : h / 2,
                a = pv.Scale.linear(0, pv.sum(data)).range(0, 2 * Math.PI);
            """ % (self.p_data, self.p_width, self.p_height))

        self.setupRootPanel()

        # The wedge, with centered label.
        self.add(pv.Wedge) \
            .data(js('data.sort(pv.reverseOrder)')) \
            .bottom(js('r')) \
            .left(js('r')) \
            .innerRadius(js('r - 40')) \
            .outerRadius(js('r')) \
            .angle(js('a')) \
            .event("mouseover", js('function() this.innerRadius(0)')) \
            .event("mouseout", js('function() this.innerRadius(r - 40)')) \
          .anchor("center").add(pv.Label) \
            .visible(js('function(d) d > .15')) \
            .textAngle(0) \
            .text(js('function(d) d.toFixed(2)'))

class LineChart(twp.PVWidget):
    p_interpolate = twc.Param(
        """How to interpolate between values. Linear interpolation ("linear")
        is the default, producing a straight line between points. For
        piecewise constant functions (i.e., step functions), either
        "step-before" or "step-after" can be specified. To draw a clockwise
        circular arc between points, specify "polar"; to draw a counter
        clockwise circular arc between points, specify "polar-reverse". To
        draw open uniform b-splines, specify "basis". To draw cardinal
        splines, specify "cardinal"; see also #tension.
        """, default='linear')

    p_line_width = twc.Param("Floating point. ", default=1.75)

    p_labels = twc.Param('list of label strings')

    def prepare(self):
        if self.p_labels and len(self.p_labels) != len(self.p_data):
           raise ValueError, \
                   "%s must have same # labels(%i) and data(%i)" % (
                       type(self).__name__,
                       len(self.p_labels),
                       len(self.p_data))

        super(LineChart, self).prepare()

        minx = min([min([l['x'] for l in d]) for d in self.p_data])
        maxx = max([max([l['x'] for l in d]) for d in self.p_data])
        miny = min([min([l['y'] for l in d]) for d in self.p_data])
        maxy = max([max([l['y'] for l in d]) for d in self.p_data])
        
        # Sizing and scales.
        self.init_js = js(
            """
            var data = %s,
                w = %i,
                h = %i,
                x = pv.Scale.linear(%f, %f).range(0, w),
                y = pv.Scale.linear(%f-1.0, %f+1.0).range(0, h),
                labels = %s;
            """ % (self.p_data, self.p_width, self.p_height,
                   minx, maxx, miny, maxy, self.p_labels ))

        self.setupRootPanel()

        # X-axis ticks.
        self.add(pv.Rule) \
            .data(js('x.ticks()')) \
            .visible(js('function(d) d > 0')) \
            .left(js('x')) \
            .strokeStyle("#eee") \
          .add(pv.Rule) \
            .bottom(-5) \
            .height(5) \
            .strokeStyle("#000") \
          .anchor("bottom").add(pv.Label) \
            .text(js('x.tickFormat'))

        # Y-axis ticks.
        self.add(pv.Rule) \
            .data(js('y.ticks(5)')) \
            .bottom(js('y')) \
            .strokeStyle(js('function(d) d ? "#eee" : "#000"')) \
          .anchor("left").add(pv.Label) \
            .text(js('y.tickFormat'))

        # The lines.
        for i in range(len(self.p_data)):
            self.add(pv.Line) \
                .data(js('data[%i]' % i)) \
                .interpolate(self.p_interpolate) \
                .left(js('function(d) x(d.x)')) \
                .bottom(js('function(d) y(d.y)')) \
                .strokeStyle(js('pv.Colors.category20().range()[%i]' % i)) \
                .lineWidth(self.p_line_width)

        if self.p_labels:
            # A legend entry for each person.
            self.add(pv.Bar) \
              .data(js('data')) \
              .top(5).left(5) \
              .width(max(map(len, self.p_labels)) * 8 + 5) \
              .height(len(self.p_labels) * 12) \
              .fillStyle('white').strokeStyle('black').lineWidth(0.4) \
            .add(pv.Dot) \
              .left(10) \
              .top(js('function() this.index * 12 + 10')) \
              .fillStyle(js('pv.Colors.category20().by(pv.index)')) \
              .strokeStyle(None) \
            .anchor("right").add(pv.Label) \
              .text(js('function() labels[this.index]'))



class StackedAreaChart(twp.PVWidget):
    p_labels = twc.Param('list of label strings')

    def prepare(self):
        if self.p_labels and len(self.p_labels) != len(self.p_data):
           raise ValueError, \
                   "%s must have same # labels(%i) and data(%i)" % (
                       type(self).__name__,
                       len(self.p_labels),
                       len(self.p_data))

        super(StackedAreaChart, self).prepare()

        # Sizing and scales.
        self.init_js = js(
            """
            var data = %s,
                w = %i,
                h = %i,
                x = pv.Scale.linear(0, 9.9).range(0, w),
                y = pv.Scale.linear(0, 14).range(0, h),
                labels = %s;
            """ % (self.p_data, self.p_width, self.p_height, self.p_labels))
        
        self.setupRootPanel()
        
        # X-axis and ticks.
        self.add(pv.Rule) \
            .data(js('x.ticks()')) \
            .visible(js('function(d) d')) \
            .left(js('x')) \
            .bottom(-5) \
            .height(5) \
          .anchor("bottom").add(pv.Label) \
            .text(js('x.tickFormat'))

        # The stack layout.
        self.add(pv.Layout.Stack) \
            .layers(js('data')) \
            .x(js('function(d) x(d.x)')) \
            .y(js('function(d) y(d.y)')) \
          .layer.add(pv.Area)

        # Y-axis and ticks.
        self.add(pv.Rule) \
            .data(js('y.ticks(3)')) \
            .bottom(js('y')) \
            .strokeStyle(js('function(d) d ? "rgba(128,128,128,.2)" : "#000"'))\
          .anchor("left").add(pv.Label) \
            .text(js('y.tickFormat'))

        if self.p_labels:
            # A legend entry for each person.
            self.add(pv.Bar) \
              .data(js('data')) \
              .top(5).left(5) \
              .width(max(map(len, self.p_labels)) * 8 + 5) \
              .height(len(self.p_labels) * 12) \
              .fillStyle('white').strokeStyle('black').lineWidth(0.4) \
            .add(pv.Dot) \
              .left(10) \
              .top(js('function() this.index * 12 + 10')) \
              .fillStyle(js('pv.Colors.category20().by(pv.index)')) \
              .strokeStyle(None) \
            .anchor("right").add(pv.Label) \
              .text(js('function() labels[this.index]'))


class GroupedBarChart(twp.PVWidget):
    p_labels = twc.Param('list of label strings')
    def prepare(self):
        if len(self.p_labels) != len(self.p_data):
           raise ValueError, 'Barchart must have same # of labels and data'

        super(GroupedBarChart, self).prepare()

        # Sizing and scales.
        self.init_js = js(
            """
            var data = %s;
            var n = data.length;
            var m = data[0].length;
            var w = %i,
                h = %i,
                x = pv.Scale.linear(0, 1.1).range(0, w),
                y = pv.Scale.ordinal(pv.range(n)).splitBanded(0, h, 4/5),
                labels = %s;
            """ % (self.p_data, self.p_width, self.p_height, self.p_labels))

        self.p_left = 7 * max([len(items) for items in self.p_labels])

        self.setupRootPanel()

        # The bars.
        bar = self.add(pv.Panel) \
            .data(js('data')) \
            .top(js('function() y(this.index)')) \
            .height(js('y.range().band')) \
          .add(pv.Bar) \
            .data(js('function(d) d')) \
            .top(js('function() this.index * y.range().band / m')) \
            .height(js('y.range().band / m')) \
            .left(0) \
            .width(js('x')) \
            .fillStyle(js('pv.Colors.category20().by(pv.index)'))

        # The value label.
        bar.anchor("right").add(pv.Label) \
            .textStyle("white") \
            .text(js('function(d) d.toFixed(1)'))

        # The variable label.
        bar._parent.anchor("left").add(pv.Label) \
            .textAlign("right") \
            .textMargin(5) \
            .text(js("function() labels[this.parent.index]"))

        # X-axis ticks.
        self.add(pv.Rule) \
            .data(js('x.ticks(5)')) \
            .left(js('x')) \
            .strokeStyle(js('function(d) d ? "rgba(255,255,255,.3)" : "#000"'))\
          .add(pv.Rule) \
            .bottom(0) \
            .height(5) \
            .strokeStyle("#000") \
          .anchor("bottom").add(pv.Label) \
            .text(js('x.tickFormat'))
