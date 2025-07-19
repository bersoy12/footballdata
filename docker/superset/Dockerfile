FROM apache/superset:latest

USER root

RUN pip install psycopg2-binary

COPY ./docker-entrypoint.sh /app/

RUN chmod +x /app/docker-entrypoint.sh

USER superset

ENTRYPOINT [ "/app/docker-entrypoint.sh" ]