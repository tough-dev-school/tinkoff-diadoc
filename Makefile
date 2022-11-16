install-dev-deps: dev-deps
	pip-sync requirements.txt dev-requirements.txt

install-deps: deps
	pip-sync requirements.txt

deps:
	pip-compile --resolver=backtracking --output-file=requirements.txt pyproject.toml

dev-deps: deps
	pip-compile --resolver=backtracking --extra=dev --output-file=dev-requirements.txt pyproject.toml

fmt:
	cd src && isort .
	cd src && black .

lint:
	dotenv-linter .env.example
	flake8 src
	cd src && mypy

test:
	cd src && pytest --dead-fixtures
	cd src && pytest -x
