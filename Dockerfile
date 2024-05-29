FROM python:3.10-slim

# needs to be set for users with manually set UID
ENV HOME=/home/alexandria

ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE alexandria.settings.django
ENV APP_HOME=/app
ENV UWSGI_INI /app/uwsgi.ini

RUN mkdir -p $APP_HOME \
  && useradd -u 901 -r alexandria --create-home \
  # all project specific folders need to be accessible by newly created user but
  # also for unknown users (when UID is set manually). Such users are in group
  # root.
  && chown -R alexandria:root $HOME \
  && chmod -R 770 $HOME \
  # This is needed because we include the alexandria folder in pyproject.toml.
  # As we don't want to copy the whole app for installing dependencies, we
  # create a fake package here.
  && mkdir $APP_HOME/alexandria \
  && touch $APP_HOME/README.md $APP_HOME/alexandria/__init__.py

WORKDIR $APP_HOME

RUN \
  --mount=type=cache,target=/var/cache/apt \
  apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev wait-for-it \
    # Default dependencies for preview-generator
    ghostscript imagemagick libfile-mimeinfo-perl libimage-exiftool-perl \
    libjpeg-dev libmagic1 libsecret-1-0 poppler-utils webp zlib1g-dev \
    # Extra dependencies for preview-generator to support office, vector and video files
    ffmpeg inkscape libreoffice \
  && rm -rf /var/lib/apt/lists/*

RUN pip install -U poetry

ARG INSTALL_DEV_DEPENDENCIES=false
COPY pyproject.toml poetry.lock $APP_HOME/
RUN if [ "$INSTALL_DEV_DEPENDENCIES" = "true" ]; then poetry install; else poetry install --without dev; fi

USER alexandria

COPY . $APP_HOME

EXPOSE 8000

CMD /bin/sh -c "wait-for-it $DATABASE_HOST:${DATABASE_PORT:-5432} -- poetry run python ./manage.py migrate && poetry run uwsgi"
