"""
TODO
"""

import tw2.core as twc
import tw2.protovis.core as twp
from tw2.protovis.core import pv

class js(twc.JSSymbol):
    def __init__(self, src):
        super(js, self).__init__(src=src)

class AreaChart(twp.PVPanel):
    p_data = twc.Param('(list) data for the chart')
    p_width = twc.Param('TODO', default=400)
    p_height = twc.Param('TODO', default=200)
    p_bottom = twc.Param('TODO', default=20)
    p_top = twc.Param('TODO', default=5)
    p_left = twc.Param('TODO', default=20)
    p_right = twc.Param('TODO', default=10)
    p_color = twc.Param('TODO', default='rgb(121,173,210)')

    def prepare(self):
        super(AreaChart, self).prepare()
        self.init_js = twc.JSSymbol(
            src="""
            var data = %s,
                w = %i,
                h = %i,
                x = pv.Scale.linear(data, function(d) d.x).range(0, w),
                y = pv.Scale.linear(0, 5).range(0, h);
            """ % (self.py_data, self.p_width, self.p_height))
                          
        self.init().width(self.p_width).height(self.p_height) \
                .bottom(self.p_bottom).top(self.p_top) \
                .left(self.p_left).right(self.p_right)

        self.add(pv.Area) \
                .data(self.py_data) \
                .bottom(1) \
                .left(js('function(d) x(d.x)')) \
                .height(twc.JSSymbol(src='function(d) y(d.y)')) \
                .fillStyle(self.p_color) \
                .anchor('top').add(pv.Line).lineWidth(3)
