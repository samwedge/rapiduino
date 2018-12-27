build:
	scripts/build_envs.sh; \
	source py3env/bin/activate; \

clean:
	rm -rf py2env; \
	rm -rf py3env; \
	rm -rf build; \
	rm -rf dist; \
	rm -rf rapiduino.egg-info; \

package:
	scripts/build_package.sh; \

test:
	py2env/bin/flake8 rapiduino; \
	py2env/bin/unit2 discover --pattern=test_*.py; \
	py3env/bin/flake8 rapiduino; \
	py3env/bin/unit2 discover --pattern=test_*.py; \

travis:
	unit2 discover --pattern=test_*.py
	flake8 rapiduino
	coverage run --source=rapiduino -m unittest2 discover && coveralls; \