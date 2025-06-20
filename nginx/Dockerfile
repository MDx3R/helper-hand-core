FROM nginx:stable-alpine

# рекомендовано https://hub.docker.com/_/nginx
COPY ./templates /etc/nginx/templates
COPY ./frontend /var/www/frontend

ENV TZ=UTC