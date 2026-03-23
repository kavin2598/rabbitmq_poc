# RabbitMQ POC Project

This repository contains a minimal RabbitMQ proof-of-concept project with:

- A RabbitMQ broker (via Docker Compose)
- A Python producer that publishes messages to a queue
- A Python consumer that reads messages from the same queue

## Project structure

- `docker-compose.yml` - Runs RabbitMQ with management UI
- `app/producer.py` - Publishes sample messages
- `app/consumer.py` - Consumes and prints messages
- `app/requirements.txt` - Python dependency list

## Prerequisites

- Docker + Docker Compose
- Python 3.11+ (for running producer/consumer outside containers)

## 1) Start RabbitMQ

```bash
docker compose up -d
```

RabbitMQ services:

- AMQP: `localhost:5672`
- Management UI: <http://localhost:15672>
- Default user/pass: `guest` / `guest`

## 2) Install Python dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r app/requirements.txt
```

## 3) Run a consumer terminal

```bash
python app/consumer.py
```

## 4) Run a producer terminal

```bash
python app/producer.py
```

You should see the consumer print the messages sent by the producer.

## Optional environment variables

Both scripts support these environment variables:

- `RABBITMQ_HOST` (default: `localhost`)
- `RABBITMQ_PORT` (default: `5672`)
- `RABBITMQ_USER` (default: `guest`)
- `RABBITMQ_PASS` (default: `guest`)
- `RABBITMQ_QUEUE` (default: `demo_queue`)

## Stop services

```bash
docker compose down
```
