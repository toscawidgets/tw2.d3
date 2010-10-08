tw2.protovis.conventional
=========================

:Author: Ralph Bean <ralph.bean@gmail.com>

.. comment: split here

.. _toscawidgets2 (tw2): http://toscawidgets.org/documentation/tw2.core/
.. _protovis: http://vis.stanford.edu/protovis/

tw2.protovis.conventional is a `toscawidgets2 (tw2)`_ wrapper for `protovis`_.

Live Demo
---------

Peep the `live demonstration <http://craftsman.rc.rit.edu/module?module=tw2.protovis.conventional>`_.

Links
-----

You can `get the source from github <http://github.com/ralphbean/tw2.protovis.conventional>`_,
check out `the PyPI page <http://pypi.python.org/pypi/tw2.protovis.conventional>`_, and
report or look into `bugs <http://github.com/ralphbean/tw2.protovis.conventional/issues/>`_.

Description
-----------

`toscawidgets2 (tw2)`_ aims to be a practical and useful widgets framework
that helps people build interactive websites with compelling features, faster
and easier. Widgets are re-usable web components that can include a template,
server-side code and JavaScripts/CSS resources. The library aims to be:
flexible, reliable, documented, performant, and as simple as possible.

`protovis`_ composes custom views of data with simple marks such as bars and dots. Unlike low-level graphics libraries that quickly become tedious for visualization, Protovis defines marks through dynamic properties that encode data, allowing inheritance, scales and layouts to simplify construction.

This module, tw2.protovis.conventional, provides `toscawidgets2 (tw2)`_ widgets that render `protovis`_ data visualizations.


Sampling tw2.protovis.conventional in the WidgetBrowser
-------------------------------------

The best way to scope out ``tw2.protovis.conventional`` is to load its widgets in the 
``tw2.devtools`` WidgetBrowser.  To see the source code that configures them,
check out ``tw2.protovis.conventional/samples.py``

To give it a try you'll need git, mercurial, python, and virtualenv.  Run:

    ``git clone git://github.com/ralphbean/tw2.protovis.conventional.git``

    ``cd tw2.protovis.conventional``

The following script will set up all the necessary tw2 dependencies in a
python virtualenv:

    ``./develop-tw2-destroy-and-setup.sh``

The following will enter the virtualenv and start up ``paster tw2.browser``:

    ``./develop-tw2-start.sh``

...and browse to http://localhost:8000/ to check it out.



