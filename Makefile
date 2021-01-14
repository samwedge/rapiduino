test:
	poetry run python -m flake8 rapiduino
	poetry run python -m mypy rapiduino
	poetry run python -m unittest discover
