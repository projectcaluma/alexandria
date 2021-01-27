FROM python:3.6.12-slim-buster@sha256:da8ff33b695949d986005fc1c5d0811e517289aefd592841bb6493dc7f49dc45

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends libpq-dev wget build-essential \
# Dependencies for preview-generator
zlib1g-dev libjpeg-dev python3-pythonmagick libmagic-dev inkscape xvfb poppler-utils libfile-mimeinfo-perl qpdf libimage-exiftool-perl ufraw-batch ffmpeg imagemagick libreoffice \
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

ARG REQUIREMENTS=requirements-prod.txt
COPY requirements-base.txt requirements-prod.txt requirements-dev.txt $APP_HOME/
RUN pip install --upgrade --no-cache-dir --requirement $REQUIREMENTS --disable-pip-version-check

USER alexandria

COPY . $APP_HOME

EXPOSE 8000

CMD /bin/sh -c "wait-for-it.sh $DATABASE_HOST:${DATABASE_PORT:-5432} -- ./manage.py migrate && uwsgi"
