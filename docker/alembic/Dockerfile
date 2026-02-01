FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1

COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY alembic /alembic
COPY alembic.ini /alembic.ini

CMD [ "alembic", "upgrade", "head" ]
