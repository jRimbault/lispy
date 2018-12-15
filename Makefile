.PHONY: env
env:
	pipenv shell

.PHONY: init
init: pipenv
	pipenv install --dev

.PHONY: freeze
freeze: init
	pipenv run pyinstaller bin/lispy -n lispy --onefile

.PHONY: pipenv
pipenv:
	command -v pipenv || python3 -m pip install --user pipenv

.PHONY: clean
clean:
	rm -r dist/ build/ lispy.spec

.PHONY: tests
tests:
	pipenv run pytest

.PHONY: help
help:
	@echo "init :"
	@echo "  initialize a development environment"
	@echo "env :"
	@echo "  open a shell inside the virtualenv"
	@echo "freeze :"
	@echo "  produce a standalone executable"
	@echo "clean :"
	@echo "  clean the files produced by the freeze"
	@echo "tests :"
	@echo "  run the test suite"
