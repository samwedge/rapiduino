build:
	virtualenv -p python2 py2env; \
	curl https://bootstrap.pypa.io/get-pip.py | py2env/bin/python; \
	py2env/bin/pip install -r requirements.txt; \

	virtualenv -p python3 py3env; \
	curl https://bootstrap.pypa.io/get-pip.py | py3env/bin/python; \
	py3env/bin/pip install -r requirements.txt; \

clean:
	rm -rf py2env; \
	rm -rf py3env; \
	rm -rf build; \
	rm -rf dist; \
	rm -rf rapiduino.egg-info; \

package:
	python setup.py sdist bdist_wheel; \

publish:
	twine upload dist/*; \

test:
	py2env/bin/flake8 rapiduino; \
	py2env/bin/unit2 discover --pattern=test_*.py; \
	py3env/bin/flake8 rapiduino; \
	py3env/bin/unit2 discover --pattern=test_*.py; \

travis:
	unit2 discover --pattern=test_*.py; \
	flake8 rapiduino; \
	coverage run --source=rapiduino -m unittest2 discover && coveralls; \