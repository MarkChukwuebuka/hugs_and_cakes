# Variables
PYTHON = uv run python
MANAGE = $(PYTHON) manage.py

.PHONY: help
help: ## Show this help message. These are the available commands that can be run on the platform in the form `make <command>`
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {gsub(/<[^>]+>/, "\033[36m&\033[0m", $$2); printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'


.PHONY: updates
updates: ## Update application to current state (db migrations, permissions etc)
	@echo "Migrating new model changes"
	$(PYTHON) manage.py makemigrations
	$(PYTHON) manage.py migrate
	@echo "Finished migrating models"

.PHONY: check
check: ## Check that everything works
	$(PYTHON) manage.py check

.PHONY: run
run: ## Check that everything works
	$(PYTHON) manage.py runserver

.PHONY: clean-pyc
clean-pyc: ## Clean pycache
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +