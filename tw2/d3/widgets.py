"""
tw2 widgets that make use of `d3 <http://mbostock.github.com/d3/>`_.
"""

import simplejson
import uuid
import warnings

import tw2.core as twc
import tw2.jquery as twj

modname = '.'.join(__name__.split('.')[:-1])

d3_js = twc.JSLink(
    modname=modname,
    filename='static/js/2.8.0/d3.v2.js',
)


class D3Widget(twc.Widget):
    template = "mako:tw2.d3.templates.d3"
    resources = [twj.jquery_js, d3_js]

    def prepare(self):
        if ':' in self.compound_id:
            # Warning.  we're forcibly overriding the user-provided id here.
            # Reason being that d3 doesn't handle edge-case selectors well.
            new_id = "d3_" + str(uuid.uuid4()).replace('-', '')
            warnings.warn("'%s' is an illegal d3 id.  Replacing with '%s'." %
                          (self.compound_id, new_id))
            self.id = self.compound_id = new_id

        super(D3Widget, self).prepare()


class BarChart(D3Widget):
    resources = D3Widget.resources + [
        twc.JSLink(modname=modname, filename="static/ext/bar.js"),
        twc.CSSLink(modname=modname, filename="static/ext/bar.css"),
    ]

    data = twc.Param("An OrderedDict of key-value pairs", default=None)
    width = twc.Param("Width of the chart in pixels.", default=960)
    height = twc.Param("Height of the chart in pixels.", default=930)
    padding = twc.Param("A list of ints [top, right, bottom, left]",
                        default=[30, 10, 10, 30])
    fmtstr = twc.Param("A format string for numeric values.",
                       default=",.0f")

    def prepare(self):

        # Check the types of everything
        int(self.width)
        int(self.height)
        str(self.fmtstr)
        self.padding = [int(ele) for ele in self.padding]

        if self.data == None:
            raise ValueError("BarChart must be provided a `data` dict")

        super(BarChart, self).prepare()

        # Munge our data so d3 can understand it
        json = [{'key': k, 'value': v} for k, v in self.data.iteritems()]

        self.add_call(twc.js_function('tw2.d3.bar')(
            self.attrs['id'],
            json,
            self.width,
            self.height,
            self.padding,
            self.fmtstr,
        ))
