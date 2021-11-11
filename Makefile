install:
	poetry install

build: install
	poetry build

package-install: build
	python3 -m pip install --user dist/*.whl --force-reinstall

lint:
	poetry run flake8 page_loader

test:
	poetry run pytest -vv --log-cli-level=DEBUG

page-loader:
	poetry run page-loader

test-coverage:
	poetry run pytest --cov=page_loader --cov-report xml --cov-config=.coveragerc

.PHONY: page-loader