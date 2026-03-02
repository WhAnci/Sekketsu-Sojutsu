FROM nginx:alpine
COPY ./nginx.conf /etc/nginx/conf.d/default.conf.template
RUN apk update && apk upgrade && apk add curl
ENTRYPOINT ["/bin/sh", "-c", "envsubst '${CONN_PRODUCT}' < /etc/nginx/conf.d/default.conf.template > /etc/nginx/conf.d/default.conf && nginx -g 'daemon off;'"]
EXPOSE 80
