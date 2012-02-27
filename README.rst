tw2.d3
======

:Author: Ralph Bean <rbean@redhat.com>

.. comment: split here

.. _toscawidgets2 (tw2): http://toscawidgets.org/documentation/tw2.core/
.. _d3: http://mbostock.github.com/d3/

tw2.d3 is a `toscawidgets2 (tw2)`_ wrapper for `d3`_.

Live Demo
---------

Peep the `live demonstration <http://tw2-demos.threebean.org/module?module=tw2.d3>`_.

Links
-----

You can `get the source from github <http://github.com/ralphbean/tw2.d3>`_,
check out `the PyPI page <http://pypi.python.org/pypi/tw2.d3>`_, and
report or look into `bugs <http://github.com/ralphbean/tw2.d3/issues/>`_.

Description
-----------

`toscawidgets2 (tw2)`_ aims to be a practical and useful widgets framework
that helps people build interactive websites with compelling features, faster
and easier. Widgets are re-usable web components that can include a template,
server-side code and JavaScripts/CSS resources. The library aims to be:
flexible, reliable, documented, performant, and as simple as possible.

`d3`_ allows you to bind arbitrary data to a Document Object Model (DOM), and
then apply data-driven transformations to the document. As a trivial example,
you can use `d3`_ to generate a basic HTML table from an array of numbers. Or, use
the same data to create an interactive SVG bar chart with smooth transitions and
interaction.  It is the successor of protovis.

This module, tw2.d3, provides `toscawidgets2 (tw2)`_ widgets that render `d3`_ data visualizations.


Sampling tw2.d3 in the WidgetBrowser
------------------------------------

The best way to scope out ``tw2.d3`` is to load its widgets in the
``tw2.devtools`` WidgetBrowser.  To see the source code that configures them,
check out ``tw2.d3/tw2/d3/samples.py``

To give it a try you'll need git, mercurial, python, and virtualenv.  Run::

    $ git clone git://github.com/ralphbean/tw2.d3.git
    $ cd tw2.d3
    $ mkvirtualenv tw2.d3
    (tw2.d3) $ pip install tw2.devtools
    (tw2.d3) $ python setup.py develop
    (tw2.d3) $ paster tw2.browser

...and browse to http://localhost:8000/ to check it out.



