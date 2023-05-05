.PHONY: install run

install:
	pip install -r requirements.txt

run:
	.venv/bin/python gameoflife.py