install-dev-deps: dev-deps
	pip-sync requirements.txt dev-requirements.txt

install-deps: deps
	pip-sync requirements.txt

deps:
	pip-compile --strip-extras --output-file=requirements.txt pyproject.toml

dev-deps: deps
	pip-compile --extra=dev --strip-extras --output-file=dev-requirements.txt pyproject.toml

fmt:
	cd src && autoflake --in-place --remove-all-unused-imports --recursive .
	cd src && isort .
	cd src && black .

lint:
	dotenv-linter env.example
	flake8 src
	cd src && mypy

test:
	cd src && pytest --dead-fixtures
	cd src && pytest -x
