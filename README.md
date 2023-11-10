# alexandria

[![Build Status](https://github.com/projectcaluma/emeis/workflows/Tests/badge.svg)](https://github.com/projectcaluma/emeis/actions?query=workflow%3ATests)
[![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen.svg)](https://github.com/projectcaluma/emeis/blob/master/setup.cfg#L50)
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/projectcaluma/alexandria)
[![License: GPL-3.0-or-later](https://img.shields.io/github/license/projectcaluma/emeis)](https://spdx.org/licenses/GPL-3.0-or-later.html)

Our goal is to implement an external document management service to hold and provide uploaded documents.
Documents can be uploaded and, depending on user access, managed by internal as well as external users.

The goal is NOT to re implement a complex [DMS](https://en.wikipedia.org/wiki/Document_management_system) but rather to have a simple and user-friendly way of managing documents with different permissions.

All User Interface interactions should be as simple as possible and easily understandable.

[Original RFC that led to alexandria](docs/original_alexandria_rfc.md)

## Getting started

### Installation

**Requirements**

- docker
- docker-compose

After installing and configuring those, download [docker-compose.yml](https://raw.githubusercontent.com/projectcaluma/alexandria/master/docker-compose.yml) and run the following commands:

```bash
# only needs to be run once
echo UID=$UID > .env

docker compose up -d
```

You can now access the api at [http://localhost:8000/api/v1/](http://localhost:8000/api/v1/).

### Example data

To load a set of categories run the following command:

```bash
make load_example_data
```

### Configuration

Document Merge Service is a [12factor app](https://12factor.net/) which means that configuration is stored in environment variables.
Different environment variable types are explained at [django-environ](https://github.com/joke2k/django-environ#supported-types).

#### Common

A list of configuration options which you need

- Django configuration
  - `SECRET_KEY`: A secret key used for cryptography. This needs to be a random string of a certain length. See [more](https://docs.djangoproject.com/en/2.1/ref/settings/#std:setting-SECRET_KEY).
  - `ALLOWED_HOSTS`: A list of hosts/domains your service will be served from. See [more](https://docs.djangoproject.com/en/2.1/ref/settings/#allowed-hosts).
  - `DATABASE_ENGINE`: Database backend to use. See [more](https://docs.djangoproject.com/en/2.1/ref/settings/#std:setting-DATABASE-ENGINE). (default: django.db.backends.postgresql)
  - `DATABASE_HOST`: Host to use when connecting to database (default: localhost)
  - `DATABASE_PORT`: Port to use when connecting to database (default: 5432)
  - `DATABASE_NAME`: Name of database to use (default: alexandria)
  - `DATABASE_USER`: Username to use when connecting to the database (default: alexandria)
  - `DATABASE_PASSWORD`: Password to use when connecting to database
- Authentication configuration
  - `OIDC_OP_USER_ENDPOINT`: Userinfo endpoint for OIDC
  - `OIDC_VERIFY_SSL`: Set to `false` if you want to disable verifying SSL certs. Useful for development
  - `OIDC_DRF_AUTH_BACKEND`: Overwrite the default authentication backend with your own
  - `ALEXANDRIA_OIDC_USER_FACTORY`: Overwrite the default user with your own
  - `ALEXANDRIA_CREATED_BY_USER_PROPERTY`: Overwrite the default user property which is used for `..._by_user` (default: username)
  - `ALEXANDRIA_CREATED_BY_GROUP_PROPERTY`: Overwrite the default group property which is used for `..._by_group` (default: group)
- Authorization configurations
  - `ALEXANDRIA_VISIBILITY_CLASSES`: Comma-separated list of classes that define visibility for all models
  - `ALEXANDRIA_PERMISSION_CLASSES`: Comma-separated list of classes that define permissions for all models
- Data validation configuration
  - `ALEXANDRIA_VALIDATION_CLASSES`: Comma-separated list of classes that define [custom validations](docs/validation.md)
- Thumbnail configuration (optional)
  - `ALEXANDRIA_ENABLE_THUMBNAIL_GENERATION`: Set to `false` to disable thumbnail generation
    - Check the docker-compose file for an example on how to set up generation with s3 hooks
  - `ALEXANDRIA_THUMBNAIL_WIDTH`: Width of generated thumbnails
  - `ALEXANDRIA_THUMBNAIL_HEIGHT`: Height of generated thumbnails
  - `ALEXANDRIA_ENABLE_CHECKSUM`: Set to `false` to disable file checksums. Checksums are calculated after upload to allow later verification (not implemented in Alexandria)

For development, you can also set the following environemnt variables to help you:

- `ALEXANDRIA_DEV_AUTH_BACKEND`: Set this to "true" to enable a fake auth backend that simulates an authenticated user. Requires `DEBUG` to be set to `True` as well.
- `DEBUG`: Set this to true for debugging during development. Never enable this in production, as it **will** leak information to the public if you do.

## Contributing

Look at our [contributing guidelines](CONTRIBUTING.md) to start with your first contribution.

## Maintainer's Handbook

Some notes for maintaining this project can be found in [the maintainer's handbook](MAINTAINING.md).
