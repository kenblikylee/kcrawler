if [ -d build ]; then rm -rf build; fi
if [ -d dist ]; then rm -rf dist; fi
if [ -d *.egg-info ]; then rm -rf *.egg-info; fi

python setup.py sdist bdist_wheel
