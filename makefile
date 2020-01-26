build-dev: clean
	virtualenv -p python3 env;
	env/bin/pip install -e .[dev];

clean:
	rm -rf env;
	rm -rf build;
	rm -rf dist;
	rm -rf rapiduino.egg-info;

package: build-dev
	env/bin/python setup.py sdist;
	env/bin/python setup.py bdist_wheel;

publish: package
	twine upload dist/*;

test: build-dev
	env/bin/python -m flake8 rapiduino;
	env/bin/python -m unittest discover;

travis:
	python -m flake8 rapiduino;
	python -m coverage run --source=rapiduino -m unittest discover && python -m coveralls;
