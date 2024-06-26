FROM python:3.11-slim-bullseye AS builder
MAINTAINER datapunt@amsterdam.nl

RUN apt update && apt install --no-install-recommends -y \
    build-essential \
    libgeos-dev \
    libpq-dev
COPY requirements.txt ./
ARG PIP_REQUIREMENTS=requirements.txt
RUN python -m pip install uwsgi
RUN python -m pip install --no-cache-dir -r $PIP_REQUIREMENTS

# Start runtime image,
FROM python:3.11-slim-bullseye
RUN useradd -U -r panorama
RUN apt update && apt install --no-install-recommends -y \
    curl \
    libgdal28 \
    libgeos-c1v5 \
    libpq5 \
    media-types \
    netcat-openbsd

# Copy python build artifacts from builder image
COPY --from=builder /usr/local/bin/ /usr/local/bin/
COPY --from=builder /usr/local/lib/python3.11/site-packages/ /usr/local/lib/python3.11/site-packages/

WORKDIR /app
COPY panorama ./
COPY deploy /deploy/

ENV DJANGO_SETTINGS_MODULE=panorama.settings DJANGO_DEBUG=false
RUN python manage.py collectstatic --noinput

EXPOSE 8000
USER panorama
CMD ["uwsgi"]
