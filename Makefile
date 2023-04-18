.PHONY: install

install:
	pip install -r requirements.txt

run:
	. .venv/bin/activate && python gameoflife.py