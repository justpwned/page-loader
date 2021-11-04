install:
	poetry install

build:
	poetry build

package-install: build
	python3 -m pip install --user dist/*.whl --force-reinstall

lint:
	poetry run flake8 page_loader

test:
	poetry run pytest -vv

page-loader:
	poetry run page-loader

test-coverage:
	poetry run pytest --cov=page_loader --cov-report xml

.PHONY: page-loader