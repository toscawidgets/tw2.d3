#!/bin/bash -e

devbase=development-deps
venv=$devbase/virtualenv-tw2.jit
$(
    rm -rf $venv
) || echo "Did not destroy $venv"

virtualenv $venv --no-site-packages

source $venv/bin/activate
pip install genshi
pushd $devbase
hg clone http://bitbucket.org/ralphbean/tw2core || echo "tw2core exists."
hg clone http://bitbucket.org/ralphbean/tw2devtools || echo "tw2devtools exists."
git clone http://github.com/ralphbean/tw2.protovis.core.git || echo "tw2.protovis.core exists."
pushd tw2core;hg pull;python setup.py develop;popd
pushd tw2devtools;hg pull;python setup.py develop;popd
pushd tw2.protovis.core;git pull;python setup.py develop;popd
popd

