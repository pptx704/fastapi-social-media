FROM python:3.13.0b2-slim

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

COPY --from=ghcr.io/ufoscout/docker-compose-wait:latest /wait /wait

# Install pip requirements
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

WORKDIR /
COPY . /

EXPOSE 8000

CMD /wait; alembic upgrade head; uvicorn main:app --host 0.0.0.0