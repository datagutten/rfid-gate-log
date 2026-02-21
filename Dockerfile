FROM python:3.14 AS builder
WORKDIR /app
COPY pyproject.toml .

RUN pip install --upgrade pip poetry poetry-plugin-export

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

FROM python:3.14
COPY --from=builder /app/wheels /wheels

RUN pip install --no-cache /wheels/*

WORKDIR /app
COPY rfid_gate_log .
COPY gunicorn.conf.py .
COPY gunicorn.conf_api.py .
CMD gunicorn

EXPOSE 80