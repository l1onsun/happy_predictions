# Makefile only for dev tasks
include .env
export

test:
	python -m pytest tests

check:
	pre-commit run -a

install:
	pip install -r requirements.txt
	pre-commit install

requirements.txt: pyproject.toml
	CUSTOM_COMPILE_COMMAND="make requirements.txt" pip-compile \
		--output-file=requirements.txt \
		--generate-hashes \
		pyproject.toml

sync:
	pip-sync requirements.txt


run:
	uvicorn happy_predictions.asgi:app