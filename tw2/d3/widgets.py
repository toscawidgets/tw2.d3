"""
tw2 widgets that make use of `d3 <http://mbostock.github.com/d3/>`_.
"""

import simplejson
import uuid

import tw2.core as twc
import tw2.jqplugins.ui as twui

modname = '.'.join(__name__.split('.')[:-1])

d3_js = twc.JSLink(
    modname=modname,
    filename='static/js/2.8.0/d3.v2.js',
)

class D3Widget(twui.base.JQueryUIWidget):
    template = "mako:tw2.d3.templates.d3"
    resources = twui.base.JQueryUIWidget.resources + [d3_js]

class BarChart(D3Widget):
    resources = D3Widget.resources + [
        twc.JSLink(modname=modname, filename="static/ext/bar.js"),
        twc.CSSLink(modname=modname, filename="static/ext/bar.css"),
    ]

    data = twc.Param("A list of {'key': key, 'value': value} dicts", default=None)

    def prepare(self):

        # Warning.  we're forcibly overriding the user-provided id here.
        # Reason being that d3 doesn't handle edge-case selectors well.
        self.id = self.compound_id = \
                "d3_" + str(uuid.uuid4()).replace('-', '')

        super(BarChart, self).prepare()

        self.add_call(twc.js_function('tw2.d3.bar')(
            self.selector,
            self.data
        ))

