install:
	poetry install

project:
	poetry run project

build:
	poetry build

publish:
	poetry publish --dry-run

package-install:
	pipx install dist/*.whl

package-install-user:
	python3 -m pip install --user dist/*.whl

activate:
	@echo "Run this command to activate virtual environment:"
	@echo "source $$(poetry env info --path)/bin/activate"

env-info:
	poetry env info

clean:
	rm -rf dist/ build/
