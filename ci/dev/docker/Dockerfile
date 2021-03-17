FROM python:3.7-stretch
LABEL maintainer="Matvey Konyaev <mat.coniaev2012@yandex.ru>"
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y wget

ENV DOCKERIZE_VERSION v0.6.1
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

RUN apt-get update -qq >/dev/null \
 && apt-get install -y \
        ca-certificates \
        wget \
        libsasl2-dev \
        libsasl2-modules-gssapi-mit \
        libnss-ldap \
        libpam-ldap \
        ldap-utils \
        slapd \
        ldapscripts \
        libldap2-dev \
        libpq-dev \
 && rm -rf /var/lib/apt/lists/* \
 && pip install -U pip wheel

COPY --chown=www-data:www-data app/build/pip/ /var/app/build/pip/
RUN pip install -r /var/app/build/pip/requirements.txt

VOLUME /var/app/
EXPOSE 8000
WORKDIR /var/app/src/

COPY --chown=www-data:www-data ci/dev/docker/entrypoint.sh /

CMD ["/entrypoint.sh"]
