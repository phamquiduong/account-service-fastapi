FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1

RUN pip install --no-cache-dir alembic psycopg2-binary

COPY alembic /alembic
COPY alembic.ini /alembic.ini

CMD [ "alembic", "upgrade", "head" ]
