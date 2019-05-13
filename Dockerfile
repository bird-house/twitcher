# vim:set ft=dockerfile:
FROM birdhouse/bird-base:latest
LABEL Description="Twitcher" Vendor="Birdhouse" Maintainer="https://github.com/bird-house/twitcher"

# Configure hostname and ports for services
ENV HTTP_PORT 8080
ENV HTTPS_PORT 8443
ENV OUTPUT_PORT 8000
ENV HOSTNAME localhost

# Ports used in birdhouse
EXPOSE 9001 $HTTP_PORT $HTTPS_PORT $OUTPUT_PORT

# for https://github.com/bird-house/twitcher/issues/51
#ENV POSTGRES_USER user
#ENV POSTGRES_PASSWORD password
#ENV POSTGRES_HOST postgres
#ENV POSTGRES_DB default
#ENV POSTGRES_PORT 5432
ENV TWITCHER_URL twitcher
ENV TWITCHER_PROTECTED_PATH /ows/proxy

ENV HOME /root
WORKDIR /opt/birdhouse/src/twitcher

##### deprecated ?
# Volume for data, cache, logfiles, configs
#VOLUME /opt/birdhouse/var/lib
#VOLUME /opt/birdhouse/var/log
#VOLUME /opt/birdhouse/etc
# Create folders required for installation
#RUN mkdir -p /opt/birdhouse/etc && chmod 755 /opt/birdhouse/etc && \
#    mkdir -p /opt/birdhouse/var/run && chmod 755 /opt/birdhouse/var/run
#RUN mkdir -p /opt/birdhouse/var/tmp/nginx/client

COPY requirements.txt setup.py twitcher/ ./
RUN python setup.py install

CMD ["pserve", "development.ini"]
