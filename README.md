# Alexandria

[![Build Status](https://github.com/projectcaluma/alexandria/workflows/Tests/badge.svg)](https://github.com/projectcaluma/alexandria/actions?query=workflow%3ATests)
[![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen.svg)](https://github.com/projectcaluma/alexandria/blob/master/pyproject.toml#L107)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![License: GPL-3.0-or-later](https://img.shields.io/github/license/projectcaluma/alexandria)](https://spdx.org/licenses/GPL-3.0-or-later.html)

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

### Usage

If alexandria is installed as a package you can use [PYTHON_API](PYTHON_API.md) for interacting with the models in an easier way.

Various additional features can be configured:

- Storage: Store uploaded content in S3, locally or anywhere else with [django-storages](https://github.com/jschneier/django-storages).

- Thumbnails: Generate small preview images for the uploaded content with [preview-generator](https://github.com/algoo/preview-generator). Package required by preview-generator must be handled by yourself when using Alexandria as a package.

- [ClamAV](https://www.clamav.net/): Virus scanning with ClamAV of uploaded content before it is saved to storage.

- [Document Merge Service](https://github.com/adfinis/document-merge-service): Conversion of DOCX/ODT files to pdf through Alexandria. Creates a new Document and File for the converted DOCX/ODT.

- WebDAV: Edit DOCX/ODT while directly saving to Alexandria storage.

- File content search: Search through the text content of uploaded data, such as PDF, DOCX or images. Alexandria extracts content with [Apache Tika](https://tika.apache.org/) and makes it searchable through [full text search](https://docs.djangoproject.com/en/dev/ref/contrib/postgres/search/). Currently only English, German, French, Italian are configured.

### Configuration

Alexandria is a [12factor app](https://12factor.net/) which means that configuration is stored in environment variables.
Different environment variable types are explained at [django-environ](https://github.com/joke2k/django-environ#supported-types).

Additional authorization and validation of the models is handled by [DGAP](https://github.com/adfinis/django-generic-api-permissions/?tab=readme-ov-file#usage---for-people-deploying-a-dgap-equipped-app).

Below is the list of configuration options which are available. Minimal example is available in [docker-compose.yml](docker-compose.yml)

#### Django configuration

- `SECRET_KEY`: A secret key used for cryptography. This needs to be a random string of a certain length. See [more](https://docs.djangoproject.com/en/2.1/ref/settings/#std:setting-SECRET_KEY).
- `ALLOWED_HOSTS`: A list of hosts/domains your service will be served from. See [more](https://docs.djangoproject.com/en/2.1/ref/settings/#allowed-hosts).
- `DATABASE_ENGINE`: Database backend to use. See [more](https://docs.djangoproject.com/en/2.1/ref/settings/#std:setting-DATABASE-ENGINE). (default: django.db.backends.postgresql)
- `DATABASE_HOST`: Host to use when connecting to database (default: localhost)
- `DATABASE_PORT`: Port to use when connecting to database (default: 5432)
- `DATABASE_NAME`: Name of database to use (default: alexandria)
- `DATABASE_USER`: Username to use when connecting to the database (default: alexandria)
- `DATABASE_PASSWORD`: Password to use when connecting to database

#### Authentication configuration

- `OIDC_OP_USER_ENDPOINT`: Userinfo endpoint for OIDC
- `OIDC_VERIFY_SSL`: Set to `false` if you want to disable verifying SSL certs. Useful for development
- `OIDC_DRF_AUTH_BACKEND`: Overwrite the default authentication backend with your own
- `ALEXANDRIA_OIDC_USER_FACTORY`: Overwrite the default user with your own
- `ALEXANDRIA_CREATED_BY_USER_PROPERTY`: Overwrite the default user property which is used for `..._by_user` (default: username)
- `ALEXANDRIA_CREATED_BY_GROUP_PROPERTY`: Overwrite the default group property which is used for `..._by_group` (default: group)
- `ALEXANDRIA_GET_USER_AND_GROUP_FUNCTION`: Overwrite the import string if further configuration how user and group are determined is needed.

#### Authorization configurations (optional)

- `ALEXANDRIA_VISIBILITY_CLASSES`: Comma-separated list of [DGAP](https://github.com/adfinis/django-generic-api-permissions/?tab=readme-ov-file#visibilities) classes that define visibility for all models
- `ALEXANDRIA_PERMISSION_CLASSES`: Comma-separated list of [DGAP](https://github.com/adfinis/django-generic-api-permissions/?tab=readme-ov-file#permissions) classes that define permissions for all models
- Data validation configuration
  - `ALEXANDRIA_VALIDATION_CLASSES`: Comma-separated list of [DGAP](https://github.com/adfinis/django-generic-api-permissions/?tab=readme-ov-file#data-validation) classes that define custom validations. A default base class is used for file validation. Extend `AlexandriaValidator` for own validations.

#### Thumbnail configuration (optional)

- `ALEXANDRIA_ENABLE_THUMBNAIL_GENERATION`: Set to `false` to disable thumbnail generation
  - Check the docker-compose file for an example on how to set up generation with s3 hooks
- `ALEXANDRIA_THUMBNAIL_WIDTH`: Width of generated thumbnails
- `ALEXANDRIA_THUMBNAIL_HEIGHT`: Height of generated thumbnails
- `ALEXANDRIA_ENABLE_CHECKSUM`: Set to `false` to disable file checksums. Checksums are calculated after upload to allow later verification (not implemented in Alexandria)

#### Storage configuration (optional)

Storage backends are configured globally. The storable object bears information on the encryption status allowing the ORM appropriate handling of the data.

- `ALEXANDRIA_FILE_STORAGE`: Set the backend for file uploads. [django-storages](https://github.com/jschneier/django-storages) is available (default: `alexandria.storages.backends.s3.S3Storage`)

Encryption:

- `ALEXANDRIA_ENABLE_AT_REST_ENCRYPTION`: Set to `true` to enable at-rest encryption of files (enabling this causes an error unless `ALEXANDRIA_ENCRYPTRION_METHOD` is set to a supported method)
- `ALEXANDRIA_ENCRYPTION_METHOD`: Define encryption method that is applied to uploaded objects. Available values depend on storage backend's capabilities (default: `None`)
  - available methods
    - None: no at-rest encryption
    - `ssec-global`: encrypt all files with the same key (requires: `ALEXANDRIA_FILE_STORAGE`: `alexandria.storages.backends.s3.S3Storage`)

Supported backends:

- `FileSystemStorage`: files are stored to the `MEDIA_ROOT` directory
- `S3Storage`: files are uploaded to the S3 object storage configured accordingly

  required configuations:

  - `ALEXANDRIA_S3_ACCESS_KEY`: identity
  - `ALEXANDRIA_S3_SECRET_KEY`: password to authorize identity
  - `ALEXANDRIA_S3_ENDPOINT_URL`: the url of the service
  - `ALEXANDRIA_S3_BUCKET_NAME`: the bucket name of the storage to access objects in path notation (not subdomain)

  The development setup features a minio service, implementing the S3 protocol.
  To use SSE-C in development make sure to generate a certificate for the minio container and set `ALEXANDRIA_S3_VERIFY` to `false`.

#### ClamAV (optional)

- `ALEXANDRIA_CLAMD_ENABLED`: Set this to `True` to enable ClamAV (virus scanner).
- `ALEXANDRIA_CLAMD_TCP_SOCKET`: ClamAV service socket
- `ALEXANDRIA_CLAMD_TCP_ADDR`: ClamAV service address

#### [Document Merge Service](https://github.com/adfinis/document-merge-service) (optional)

- `ALEXANDRIA_ENABLE_PDF_CONVERSION`: Set this to `True` to enable the pdf conversion endpoint.
- `ALEXANDRIA_DMS_URL`: URL where the document merge service is running

#### WebDAV (optional)

- `ALEXANDRIA_USE_MANABI`: Set to `true` to enable WebDAV via Manabi
- `ALEXANDRIA_MANABI_DAV_URL_PATH`: Set the path segement where WebDAV is being served
- `ALEXANDRIA_MANABI_ALLOWED_MIMETYPES`: List of which mime types can be served through WebDAV. (default: docx, xlsx)
- `ALEXANDRIA_MANABI_DAV_URI_SCHEMES`: Dictionary of which mime types will be mapped to which WebDAV URI scheme. (default: docx, xlsx for editing in MS Word / Excel)
- `MANABI_SHARED_KEY`: Can be generated with:

```py
import manabi
manabi.keygen()
```

If you want to enable WebDAV for e.g. MS Powerpoint files you can do that by configuring `ALEXANDRIA_MANABI_ALLOWED_MIMETYPES` and `ALEXANDRIA_MANABI_DAV_URI_SCHEMES`:

```py
ALEXANDRIA_MANABI_ALLOWED_MIMETYPES = [
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "application/vnd.openxmlformats-officedocument.presentationml.presentation", # New
]
ALEXANDRIA_MANABI_DAV_URI_SCHEMES = {
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "ms-word:ofe|u|",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": "ms-excel:ofe|u|",
    "application/vnd.openxmlformats-officedocument.presentationml.presentation": "ms-powerpoint:ofe|u|" # New, see https://learn.microsoft.com/en-us/office/client-developer/office-uri-schemes for more information
}
```

#### File content search (optional)

- `ALEXANDRIA_ENABLE_CONTENT_SEARCH`: Set to `True` to enable file content extraction
- `ALEXANDRIA_ISO_639_TO_PSQL_SEARCH_CONFIG`: Mapping from language code from tika to django search vector language config. Also defines which languages are supported by the search. (default: `{"en":"english","de":"german","fr":"french","it":"italian"}`)
- `ALEXANDRIA_CONTENT_SEARCH_TYPE`: Django full text search type. (default: phrase)

#### Celery (optional)
For checksums and file content search [celery](https://docs.celeryq.dev) with a redis broker is used.

- `REDIS_HOST`: Redis host (default: redis)
- `REDIS_PORT`: Redis port (default: 6379)
- `REDIS_USER`: Redis user (default: default)
- `REDIS_PASSWORD`: Redis password (default: redis)
- `CELERY_BROKER_URL`: Broker url (default: `redis://{REDIS_USER}:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/0`)
- `CELERY_TASK_ACKS_LATE`: Tasks only are marked complete after finishing (default: True)
- `CELERY_TASK_SOFT_TIME_LIMIT`: Prevents task existing forever (default: 60)

#### Development

For development, you can also set the following environemnt variables to help you:

- `ALEXANDRIA_DEV_AUTH_BACKEND`: Set this to "true" to enable a fake auth backend that simulates an authenticated user. Requires `DEBUG` to be set to `True` as well.
- `DEBUG`: Set this to true for debugging during development. Never enable this in production, as it **will** leak sensitive information to the public if you do.

## Contributing

Look at our [contributing guidelines](CONTRIBUTING.md) to start with your first contribution.

## Maintainer's Handbook

Some notes for maintaining this project can be found in [the maintainer's handbook](MAINTAINING.md).
