"""
tw2 widgets that make use of `d3 <http://mbostock.github.com/d3/>`_.
"""

import simplejson

import tw2.core as twc

modname = '.'.join(__name__.split('.')[:-1])

d3_js = twc.JSLink(
    modname=modname,
    filename='static/js/core/d3.v2.min.js',
)

class D3Widget(twc.Widget):
    template = "mako:tw2.d3.templates.d3"
    resources = [d3_js]

class BarChart(D3Widget):
    resources = D3Widget.resources + [
        twc.JSLink(
            modname=modname,
            filename="static/js/widgets/bar.js",
        ),
    ]

    data = twc.Param("A list of {'key': key, 'value': value} dicts", default=None)

    def prepare(self):
        super(BarChart, self).prepare()
        json = simplejson.dumps(self.data)
        self.add_call(twc.js_function('tw2.d3.bar')(json))

