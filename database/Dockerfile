FROM postgres:alpine
LABEL authors="Dmitriy Panin"

ENV POSTGRES_USER=admin
ENV POSTGRES_PASSWORD=admin_password

COPY ./setup_db.sh /docker-entrypoint-initdb.d/

EXPOSE 5432
