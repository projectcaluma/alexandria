# alexandria

[![Build Status](https://travis-ci.com/projectcaluma/alexandria.svg?branch=master)](https://travis-ci.com/projectcaluma/alexandria)
[![Pyup](https://pyup.io/repos/github/projectcaluma/alexandria/shield.svg)](https://pyup.io/account/repos/github/projectcaluma/alexandria/)
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/projectcaluma/alexandria)

Our goal is to implement an external document management service to hold and provide uploaded documents.
Documents can be uploaded and, depending on user access, managed by internal as well as external users.

The goal is NOT to re implement a complex [DMS](https://en.wikipedia.org/wiki/Document_management_system) but rather to have a simple and user-friendly way of managing documents with different permissions.

All User Interface interactions should be as simple as possible and easily understandable.

[Original RFC that led to alexandria](docs/original_alexandria_rfc.md)

## Getting started

### Installation

**Requirements**
* docker
* docker-compose

After installing and configuring those, download [docker-compose.yml](https://raw.githubusercontent.com/projectcaluma/alexandria/master/docker-compose.yml) and run the following command:

```bash
docker-compose up -d
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

* Django configuration
  * `SECRET_KEY`: A secret key used for cryptography. This needs to be a random string of a certain length. See [more](https://docs.djangoproject.com/en/2.1/ref/settings/#std:setting-SECRET_KEY).
  * `ALLOWED_HOSTS`: A list of hosts/domains your service will be served from. See [more](https://docs.djangoproject.com/en/2.1/ref/settings/#allowed-hosts).
  * `DATABASE_ENGINE`: Database backend to use. See [more](https://docs.djangoproject.com/en/2.1/ref/settings/#std:setting-DATABASE-ENGINE). (default: django.db.backends.postgresql)
  * `DATABASE_HOST`: Host to use when connecting to database (default: localhost)
  * `DATABASE_PORT`: Port to use when connecting to database (default: 5432)
  * `DATABASE_NAME`: Name of database to use (default: alexandria)
  * `DATABASE_USER`: Username to use when connecting to the database (default: alexandria)
  * `DATABASE_PASSWORD`: Password to use when connecting to database
* Authentication configuration
  * `OIDC_OP_USER_ENDPOINT`: Userinfo endpoint for OIDC
  * `OIDC_VERIFY_SSL`: Set to `false` if you want to disable verifying SSL certs. Useful for development
* Authorization configurations
  * `VISIBILITY_CLASSES`: Comma-separated list of classes that define visibility for all models
  * `PERMISSION_CLASSES` Comma-separated list of classes that define permissions for all models
## Contributing

Look at our [contributing guidelines](CONTRIBUTING.md) to start with your first contribution.
