FROM python:3.10-slim-bookworm AS base

ENV DJANGO_SETTINGS_MODULE=alexandria.settings.django \
    PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

RUN \
  --mount=type=cache,target=/var/cache/apt \
  apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev gettext wait-for-it \
    # Default dependencies for preview-generator
    ghostscript imagemagick libfile-mimeinfo-perl libimage-exiftool-perl \
    libjpeg-dev libmagic1 libsecret-1-0 poppler-utils webp zlib1g-dev \
    # Extra dependencies for preview-generator to support office, vector and video files
    ffmpeg inkscape libreoffice \
  && rm -rf /var/lib/apt/lists/* \
  && useradd -m -r -u 1001 alexandria

EXPOSE 8000

FROM base AS build

WORKDIR /app

COPY . ./

ENV POETRY_NO_INTERACTION=1

RUN pip install -U poetry

FROM build AS wheel

WORKDIR /app

RUN poetry build -f wheel && mv ./dist/*.whl /tmp/

FROM build AS dev

RUN poetry config virtualenvs.create false \
 && poetry install

USER 1001

CMD ["sh", "-c", "wait-for-it db:5432 -- ./manage.py migrate && ./manage.py runserver_plus --nostatic 0.0.0.0:8000"]

FROM base AS prod

WORKDIR /app

COPY manage.py /usr/local/bin
COPY --from=wheel /tmp/*.whl /tmp/

RUN pip install /tmp/*.whl && rm /tmp/*.whl

USER 1001

CMD ["sh", "-c", "wait-for-it $DATABASE_HOST:${DATABASE_PORT:-5432} -- ./manage.py migrate && gunicorn --workers 10 --access-logfile - --limit-request-line 16384 --bind :8000 alexandria.wsgi"]
