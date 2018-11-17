FROM python:3.6-slim

RUN pip install pytest

WORKDIR /test-retry

COPY requirements.txt .
RUN pip install -r requirements.txt