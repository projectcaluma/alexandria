FROM python:3.8-slim-buster

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends libpq-dev wget build-essential \
# Dependencies for preview-generator
zlib1g-dev libjpeg-dev python3-pythonmagick libmagic-dev inkscape xvfb poppler-utils libfile-mimeinfo-perl qpdf \
libimage-exiftool-perl ufraw-batch ffmpeg imagemagick libreoffice scribus \
&& wget -q https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh -P /usr/local/bin \
&& chmod +x /usr/local/bin/wait-for-it.sh \
&& mkdir -p /app \
&& useradd -u 901 -r alexandria --create-home \
# all project specific folders need to be accessible by newly created user but also for unknown users (when UID is set manually). Such users are in group root.
&& chown -R alexandria:root /home/alexandria \
&& chmod -R 770 /home/alexandria


RUN apt-get update && apt-get install -y --no-install-recommends \
  # needed for psycopg2
  libpq-dev

# needs to be set for users with manually set UID
ENV HOME=/home/alexandria

ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE alexandria.settings
ENV APP_HOME=/app
ENV UWSGI_INI /app/uwsgi.ini

RUN pip install -U poetry

ARG INSTALL_DEV_DEPENDENCIES=false
COPY pyproject.toml poetry.lock $APP_HOME/
RUN if [ "$INSTALL_DEV_DEPENDENCIES" = "true" ]; then poetry install; else poetry install --no-dev; fi

USER alexandria

COPY . $APP_HOME

EXPOSE 8000

CMD /bin/sh -c "wait-for-it.sh $DATABASE_HOST:${DATABASE_PORT:-5432} -- poetry run python ./manage.py migrate && uwsgi"
