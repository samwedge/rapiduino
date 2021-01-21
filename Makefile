test:
	poetry run coverage run --source=rapiduino -m pytest tests
	# mypy 0.790 bug means it isn't recursive if dir isn't a python package
	poetry run mypy rapiduino tests/test_boards tests/test_communication tests/test_components
	poetry run flake8 rapiduino tests
	poetry run black --check --diff --color rapiduino tests
	poetry run isort --check --diff --color rapiduino tests
	poetry run coverage html
	poetry run coverage report

fix:
	poetry run black rapiduino
	poetry run black tests
	poetry run isort rapiduino
	poetry run isort tests