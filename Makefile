.PHONY: docs
init:
	pip install -r requirements.txt
test:
	tox

flake8:
	flake8 market

ci:
	coverage erase && coverage run -m unittest discover && coverage xml -o report.xml

coverage:
	coverage erase && coverage run -m unittest discover && coverage html

docs:
	cd docs && make html
