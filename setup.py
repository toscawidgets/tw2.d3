from setuptools import setup, find_packages

f = open('README.rst')
long_description = f.read().strip()
long_description = long_description.split('split here', 1)[1]
f.close()

install_requires=[
    "tw2.core",
    "tw2.jquery",
]

import sys
if sys.version_info[0] == 2 and sys.version_info[1] < 7:
    install_requires.extend([
        "ordereddict",
    ])

setup(
    name='tw2.d3',
    version='0.0.2a1',
    description='toscawidgets2 wrapper for d3 (data-driven documents)',
    long_description=long_description,
    author='Ralph Bean',
    author_email='rbean@redhat.com',
    url='http://github.com/ralphbean/tw2.d3',
    install_requires=[
        "tw2.core",
        "tw2.jquery",
    ],
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages = ['tw2'],
    zip_safe=False,
    include_package_data=True,
    entry_points="""
        [tw2.widgets]
        # Register your widgets so they can be listed in the WidgetBrowser
        tw2.d3 = tw2.d3
    """,
    keywords = [
        'toscawidgets.widgets',
    ],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Environment :: Web Environment :: ToscaWidgets',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Widget Sets',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: JavaScript',
    ],
)
