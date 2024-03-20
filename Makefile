.DEFAULT_GOAL := help

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort -k 1,1 | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: build
build: ## Build the development server
	@docker compose build --pull

.PHONY: start
start: ## Start the development server
	@docker compose up -d --build

.PHONY: test
test: ## Test the backend
	@docker compose run --rm alexandria poetry run pytest --no-cov-on-fail --cov --create-db -vv

.PHONY: lint
lint: ## Lint the backend
	@docker compose run --rm alexandria sh -c "poetry run black --check . && poetry run flake8"

.PHONY: bash
bash: ## Shell into the backend
	@docker compose run --rm alexandria bash

.PHONY: shell_plus
shell_plus: ## Run shell_plus
	@docker compose run --rm alexandria poetry run python ./manage.py shell_plus

.PHONY: debug-alexandria
debug-alexandria: ## start a api container with service ports for debugging
	@docker compose stop alexandria
	@echo "Run 'poetry run python manage.py runserver 0:8000' to start the debugging server"
	@docker compose run --rm --user root --use-aliases --service-ports alexandria bash


.PHONY: makemigrations
makemigrations: ## Make django migrations
	@docker compose run --rm alexandria poetry run python ./manage.py makemigrations

.PHONY: migrate
migrate: ## Migrate django
	@docker compose run --rm alexandria poetry run python ./manage.py migrate

.PHONY: dbshell
dbshell: ## Start a psql shell
	@docker compose exec db psql -Ualexandria

.PHONY: load_example_data
load_example_data: ## Load a set of example data
	@docker compose run --rm alexandria poetry run python ./manage.py loaddata initial_data.json

.PHONY: flush
flush: ## Flush the database
	@docker compose exec alexandria poetry run python ./manage.py flush --no-input

.PHONY: dump
dump: ## dump alexandria data
	@docker compose run --rm alexandria poetry run python ./manage.py dumpdata alexandria_core | jq > initial_data.json
