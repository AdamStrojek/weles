FROM python:3.9-alpine

MAINTAINER Adam Strojek <adam@strojek.info>

RUN apk add --upgrade --no-cache \
    bash \
    curl \
    freetype-dev \
    gettext \
    libjpeg \
    libstdc++ \
    py3-pip \
    postgresql-client \
    postgresql-contrib && \
    apk add --no-cache --virtual .build-dependencies \
    build-base \
    jpeg-dev \
    libffi-dev \
    linux-headers \
    freetype-dev \
    python3-dev \
    zlib-dev \
    postgresql-dev

# RUN pip install --upgrade pip && pip install wheel==0.32.3

ENV WAITFORIT_VERSION="v2.4.1"
RUN curl -o /usr/local/bin/waitforit -sSL https://github.com/maxcnunes/waitforit/releases/download/$WAITFORIT_VERSION/waitforit-linux_amd64 && \
    chmod +x /usr/local/bin/waitforit

WORKDIR /usr/src/app

COPY requirements/*.txt /tmp/requirements/
RUN pip install -r /tmp/requirements/dev.txt && rm -rf /tmp/requirements

RUN apk del .build-dependencies

COPY . .

RUN python manage.py collectstatic --noinput

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]
