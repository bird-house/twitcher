# vim:set ft=dockerfile:
FROM python:3.7-alpine
LABEL Description="Twitcher" Vendor="Birdhouse" Maintainer="https://github.com/bird-house/twitcher"

# Configure hostname and ports for services
ENV HTTP_PORT 8080
ENV HTTPS_PORT 8443
ENV OUTPUT_PORT 8000
ENV HOSTNAME localhost
EXPOSE 9001 $HTTP_PORT $HTTPS_PORT $OUTPUT_PORT

ENV HOME /root
ENV TWITCHER_DIR /opt/birdhouse/src/twitcher
WORKDIR $TWITCHER_DIR

# copy basic requirements/references and build dependencies
# will be skipped if only source code has been updated
COPY \
    requirements* \
    setup.py \
    README.rst \
    CHANGES.rst \
    $TWITCHER_DIR/
COPY \
    twitcher/__init__.py \
    twitcher/__version__.py \
    $TWITCHER_DIR/twitcher/
RUN apk update \
    && apk add \
        bash \
        libxslt-dev \
        libxml2 \
        libffi-dev \
        openssl-dev \
    && apk add --virtual .build-deps \
        python-dev \
        gcc \
        musl-dev \
    && pip install --no-cache-dir --upgrade pip setuptools \
    && pip install --no-cache-dir -e $TWITCHER_DIR \
    && apk --purge del .build-deps

# copy source code and install it
COPY ./ $TWITCHER_DIR
RUN pip install --no-dependencies -e $TWITCHER_DIR

CMD ["pserve", "development.ini"]
