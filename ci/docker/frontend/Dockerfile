FROM node:14-alpine
LABEL maintainer="Matvey Konyaev <mat.coniaev2012@yandex.ru>"

RUN apk update && apk upgrade
RUN mkdir -p /var/app/
WORKDIR /var/app/
VOLUME /var/app
ENV HOST=0.0.0.0
ENV PORT=$FRONTEND_EXT_PORT

COPY ci/docker/frontend/entrypoint.sh /

CMD ["/entrypoint.sh"]