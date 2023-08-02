# Contributing

Contributions to alexandria are very welcome! Best have a look at the open [issues](https://github.com/projectcaluma/alexandria)
and open a [GitHub pull request](https://github.com/projectcaluma/alexandria/compare). See instructions below how to setup development
environment. Before writing any code, best discuss your proposed change in a GitHub issue to see if the proposed change makes sense for the project.

## Setup development environment

### Clone

To work on alexandria you first need to clone

```bash
git clone https://github.com/projectcaluma/alexandria.git
cd alexandria
```

### Open Shell

Once it is cloned you can easily open a shell in the docker container to
open an development environment.

```bash
# needed for permission handling
# only needs to be run once
echo UID=$UID > .env
# open shell
docker compose run --rm alexandria bash
```

### Testing

Once you have shelled in docker container as described above
you can use common python tooling for formatting, linting, testing
etc.

```bash
# linting
poetry run flake8
# format code
poetry run black .
# running tests
poetry run pytest
# create migrations
poetry run ./manage.py makemigrations
```

Writing of code can still happen outside the docker container of course.

### Install new requirements

In case you're adding new requirements you simply need to build the docker container
again for those to be installed and re-open shell.

```bash
docker compose build --pull
```

### Setup pre commit

Pre commit hooks is an additional option instead of executing checks in your editor of choice.

First create a virtualenv with the tool of your choice before running below commands:

```bash
poetry install
poetry run pre-commit install --hook=pre-commit
poetry run pre-commit install --hook=commit-msg
```
