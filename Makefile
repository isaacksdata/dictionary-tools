# Makefile

format-black:
	@black .

format-isort:
	@isort .

lint-black:
	@black . --check

lint-isort:
	@isort . --check

lint-flake8:
	@flake8 ./

lint-mypy:
	@mypy ./dict_tools

lint-mypy-report:
	@mypy ./dict_tools --html-report ./mypy_html

format: format-black format-isort
lint: lint-flake8 lint-mypy