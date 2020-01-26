build-dev: clean
	virtualenv -p python2 py2env; \
	py2env/bin/pip install -e .[test]; \

	virtualenv -p python3 py3env; \
	py3env/bin/pip install -e .[test]; \

clean:
	rm -rf py2env; \
	rm -rf py3env; \
	rm -rf build; \
	rm -rf dist; \
	rm -rf rapiduino.egg-info; \

package: build-dev
	py3env/bin/python setup.py sdist; \
	py3env/bin/python setup.py bdist_wheel; \

publish: package
	twine upload dist/*; \

test: build-dev
	py2env/bin/flake8 rapiduino; \
	py2env/bin/unit2 discover --pattern=test_*.py; \
	py3env/bin/flake8 rapiduino; \
	py3env/bin/unit2 discover --pattern=test_*.py; \

travis:
	unit2 discover --pattern=test_*.py; \
	flake8 rapiduino; \
	coverage run --source=rapiduino -m unittest2 discover && coveralls; \